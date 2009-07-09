"""
QuickBooks Merchant Services API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl, logging, traceback, datetime
from pyqbms.requests.base import QuickBooksRequestBase
from pyqbms.requests.qbms.exceptions import QBMSException, QBMSSignonException
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement

QBMS_VERSION = '2.0'
STATUS_SUCCESS = 0
SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'



class QBMSRequest(QuickBooksRequestBase):
    qbms_version = QBMS_VERSION
    rq_aggregate_type = QuickBooksRequestAggregate
    rs_aggregate_type = QuickBooksResponseAggregate

    def init(self, cert_path=None, *args, **kwargs):
        self.cert_path = cert_path
        self.rq_aggregate = self.rq_aggregate_type(*args, **kwargs)

    def build_element_tree(self):
        self.qbmsxml_el = Element('QBMSXML')
        self.signon_msgs_rq_el = SubElement(self.qbmsxml_el, 'SignonMsgsRq')
        return self.qbmsxml_el

    def build_request_xml_headers(self):    
        headers = super(QBMSRequest, self).build_request_xml_headers()
        return headers + '\n<?qbmsxml version="%s"?>' % self.qbms_version

    def build_headers(self):
        headers = super(QBMSRequest, self).build_headers()
        headers.append('Content-type: application/x-qbmsxml')
        return headers

    def build_request(self):
        request = super(QBMSRequest, self).build_request()
        if self.cert_path:
            request.setopt(pycurl.SSLCERT, self.cert_path)
        return request
    
    def parse_response(self):
        super(QBMSRequest, self).parse_response()
        self.rs_aggregate_el = self.response_tree.find('.//%s' % self.rs_aggregate_type.__name__)
        self.response = self.rs_aggregate_type(element = self.rs_aggregate_el)
        if self.response.status_code is not STATUS_SUCCESS:
            if self.response.status_severity == SEVERITY_ERROR:
                logging.error(self.response.status_message)
                raise QBMSException(self.response.status_message)
            elif self.response.status_severity == SEVERITY_WARNING:
                logging.warning(self.response.status_message)
        return self.response
                    
            


class QBMSXMLMsgsRequest(QBMSRequest):
    def init(self, signon_msg_el=None, *args, **kwargs):
        self.signon_msg_el = signon_msg_el
        return super(QBMSXMLMsgsRequest, self).init(*args, **kwargs)

    def build_element_tree(self):
        tree =  super(QBMSXMLMsgsRequest, self).build_element_tree()
        if self.signon_msg_el:
            self.signon_msgs_rq_el.append(self.signon_msg_el)
        self.qbms_xml_msgs_rq_el = SubElement(self.qbmsxml_el, 'QBMSXMLMsgsRq')
        self.qbms_xml_msgs_rq_el.append(self.rq_aggregate.element)
        return tree



