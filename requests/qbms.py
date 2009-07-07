"""
QuickBooks Merchant Services API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl, logging, traceback, datetime
from pyqbms.requests.base import QuickBooksRequestBase
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms.datatypes.signon import SignonAppCertRq, SignonAppCertRs, SignonTicketRq
from pyqbms.datatypes.signon import SignonDesktopRq, SignonDesktopRs
from pyqbms.datatypes.credit_card import CustomerCreditCardChargeRq, CustomerCreditCardChargeRs
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement


QBMS_VERSION = '2.0'
QBMS_PTC_URL = "https://merchantaccount.ptc.quickbooks.com/j/AppGateway"
QBMS_LIVE_URL = "https://merchantaccount.quickbooks.com/j/AppGateway"
QBMS_CERT_PATH = 'qbms.pem'
QBMS_LANGUAGE = 'English'

QBMS_TEST_MODE = True

QBMS_APP_ID = ''
QBMS_APP_VERSION = ''

class QBMSException(Exception): pass

class QBMSSignonException(QBMSException): pass


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
        print self.response.to_xml() 


class SignonAppCertRequest(QBMSRequest):
    rq_aggregate_type = SignonAppCertRq
    rs_aggregate_type = SignonAppCertRs

    def build_element_tree(self):
        tree =  super(SignonAppCertRequest, self).build_element_tree()
        self.signon_msgs_rq_el.append(self.rq_aggregate.element)
        return tree
        

class SignonDesktopRequest(QBMSRequest):
    rq_aggregate_type = SignonDesktopRq
    rs_aggregate_type = SignonDesktopRs

    def build_element_tree(self):
        tree =  super(SignonDesktopRequest, self).build_element_tree()
        self.signon_msgs_rq_el.append(self.rq_aggregate.element)
        return tree
        

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


class CustomerCreditCardChargeRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardChargeRq
    rs_aggregate_type = CustomerCreditCardChargeRs


class QBMSRequestorBase(object):
    def __init__(self, app_id, app_ver, application_login, connection_ticket, 
            session_ticket=None, language=QBMS_LANGUAGE, qbms_url=QBMS_PTC_URL):
        self.app_id = app_id
        self.app_ver = app_ver
        self.application_login = application_login
        self.connection_ticket = connection_ticket
        self.session_ticket = session_ticket
        self.language = language
        self.qbms_url = qbms_url

    def get_is_signed_on(self):
        if self.session_ticket:
            return True
        return False
    is_signed_on = property(get_is_signed_on)

    def build_signon_msg_el(self):
        if not self.is_signed_on:
            self.signon()

        signon_ticket_rq = SignonTicketRq(session_ticket=self.session_ticket,
            client_date_time=datetime.datetime.today())
        return signon_ticket_rq.element

    def signon(self):
        raise Exception("Not implemented")

    def build_request(self, request_class, *args, **kwargs):
        kwargs['signon_msg_el'] = self.build_signon_msg_el()
        if not 'url' in kwargs:
            kwargs['url'] = self.qbms_url
        return request_class(*args, **kwargs)

    def perform_request(self, request):
        request.perform()
        return request

    def do_request(self, request_class, *args, **kwargs):
        request = self.build_request(request_class, *args, **kwargs)
        self.perform_request(request)
        return request

    def charge_credit_card(self, *args, **kwargs): 
        return self.do_request(CustomerCreditCardChargeRequest, *args, **kwargs)


class QBMSDesktopRequestor(QBMSRequestorBase):
    def signon(self):
        logging.info('Performing Desktop Signon')
        request = SignonDesktopRequest(
            url = self.qbms_url,
            client_date_time=datetime.datetime.today(),
            application_login = self.application_login,
            # app_id = self.app_id,
            # app_ver = self.app_ver,
            # language = self.language,
            connection_ticket = self.connection_ticket
        )
        self.perform_request(request)
        self.session_ticket = request.response.session_ticket
        logging.info('Successful Desktop Signon')
        return request.response



class QBMSHostedRequestor(QBMSRequestorBase):
    def signon(self):
        logging.info('Performing Hosted Model Signon')
        request = SignonAppCertRequest(
            url = self.qbms_url,
            client_date_time=datetime.datetime.today(),
            application_login = self.application_login,
            # app_id = self.app_id,
            # app_ver = self.app_ver,
            # language = self.language,
            connection_ticket = self.connection_ticket
        )
        self.perform_request(request)
        print 'Status code: %r' %  request.response.status_code
        print 'Status severity: %r' %  request.response.status_severity
        print 'Status message: %r' %  request.response.status_message
        return request

    def do_request(self, *args, **kwargs):
        try:
            return super(QBMSHostedRequestor, self).do_request(*args, **kwargs)
        except QBMSSignonException, e:
            logging.warning(traceback.format_exc())
            self.session_ticket = None
            self.signon()
            return super(QBMSHostedRequestor, self).do_request(*args, **kwargs)
              

    

        
