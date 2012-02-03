"""
QuickBooks Merchant Services API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl, logging, traceback, datetime
from pyqbms.requests.base import QuickBooksRequestBase, QuickBooksRequestError
from pyqbms.requests.qbms.exceptions import QBMSException, QBMSSignonException, QBMSErrorType
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms.datatypes.signon import SignonTicketRs, SignonAppCertRs, SignonDesktopRs
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement

QBMS_VERSION = '4.1'
STATUS_SUCCESS = 0

SEVERITY_INFO = 'INFO'
SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'


log = logging.getLogger(__name__)


class QBMSRequest(QuickBooksRequestBase):
    """
    Encapsulation of request generation, sending, and parsing

    A QBMSRequest instance is created for each request
    """

    qbms_version = QBMS_VERSION
    rq_aggregate_type = QuickBooksRequestAggregate
    rs_aggregate_type = QuickBooksResponseAggregate

    signon_rs_aggregate_types = [
        SignonTicketRs,
        SignonAppCertRs,
        SignonDesktopRs
    ]

    def init(self, cert_path=None, *args, **kwargs):
        self.signon_response = None
        self.cert_path = cert_path
        self.rq_aggregate = self.rq_aggregate_type(*args, **kwargs)

    def build_element_tree(self):
        """Build an ElementTree representation of the request to send"""
        self.qbmsxml_el = Element('QBMSXML')
        self.signon_msgs_rq_el = SubElement(self.qbmsxml_el, 'SignonMsgsRq')
        return self.qbmsxml_el

    def build_request_xml_headers(self):
        """Return a string containing headers not included in the ElementTree representation"""
        headers = super(QBMSRequest, self).build_request_xml_headers()
        return headers + '\n<?qbmsxml version="%s"?>' % self.qbms_version

    def build_headers(self):
        """Build list of headers to send via pycurl"""
        headers = super(QBMSRequest, self).build_headers()
        headers.append('Content-type: application/x-qbmsxml')
        return headers

    def build_request(self):
        """Build a pycurl object for this request"""
        request = super(QBMSRequest, self).build_request()
        if self.cert_path:
            request.setopt(pycurl.SSLCERT, self.cert_path)
        return request

    def parse_signon_response(self):
        """Locate and parse the signon response aggregate"""
        for aggregate_type in self.signon_rs_aggregate_types:
            self.signon_rs_aggregate_el = self.response_tree.find('.//%s' % aggregate_type.__name__)
            if self.signon_rs_aggregate_el is not None:
                self.signon_response = aggregate_type(element = self.signon_rs_aggregate_el)
                if self.signon_response.status_code != STATUS_SUCCESS:
                    if self.signon_response.status_severity == SEVERITY_ERROR:
                        raise QBMSErrorType.from_rs(self.signon_response)
                    elif self.signon_response.status_severity == SEVERITY_WARNING:
                        log.warning(self.signon_response.status_message)
                break
        return self.signon_response

    def parse_response(self):
        """Locate and parse the response aggregate(s)"""
        super(QBMSRequest, self).parse_response()
        self.parse_signon_response()
        self.rs_aggregate_el = self.response_tree.find('.//%s' % self.rs_aggregate_type.__name__)
        self.response = self.rs_aggregate_type(element = self.rs_aggregate_el)
        if self.response.status_code != STATUS_SUCCESS:
            if self.response.status_severity == SEVERITY_ERROR:
                log.error(self.response.status_message)
                raise QBMSErrorType.from_rs(self.response)
            elif self.response.status_severity == SEVERITY_WARNING:
                log.warning(self.response.status_message)
        return self.response


class QBMSXMLMsgsRequest(QBMSRequest):
    """
    QBMS Request containing a QBMSXMLMsgsRq element
    """
    def init(self, signon_msg_el=None, *args, **kwargs):
        self.signon_msg_el = signon_msg_el
        return super(QBMSXMLMsgsRequest, self).init(*args, **kwargs)

    def build_element_tree(self):
        """Build an ElementTree representation of the request to send"""
        tree =  super(QBMSXMLMsgsRequest, self).build_element_tree()
        if self.signon_msg_el is not None:
            self.signon_msgs_rq_el.append(self.signon_msg_el)
        self.qbms_xml_msgs_rq_el = SubElement(self.qbmsxml_el, 'QBMSXMLMsgsRq')
        self.qbms_xml_msgs_rq_el.append(self.rq_aggregate.element)
        return tree
