"""
QuickBooks Merchant Services API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl, logging
from pyqbms.requests.base import QuickBooksRequestBase
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms.datatypes.signon import SignonAppCertRq, SignonAppCertRs, SignonTicketRq
from pyqbms.datatypes.credit_card import CustomerCreditCardChargeRq, CustomerCreditCardChargeRs
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement


QBMS_VERSION = '2.0'
QBMS_URL = "https://merchantaccount.ptc.quickbooks.com/j/AppGateway"
QBMS_CERT_PATH = 'qbms.pem'
QBMS_LANGUAGE = 'English'

QBMS_APP_ID = ''
QBMS_APP_VERSION = ''


class QBMSRequest(QuickBooksRequestBase):
    qbms_version = QBMS_VERSION
    rq_aggregate_type = QuickBooksRequestAggregate
    rs_aggregate_type = QuickBooksResponseAggregate

    def init(self, *args, **kwargs):
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
        request.setopt(pycurl.SSLCERT, QBMS_CERT_PATH)
        return request


class SignonAppCertRequest(QBMSRequest):
    rq_aggregate_type = SignonAppCertRq
    rs_aggregate_type = SignonAppCertRs

    def build_element_tree(self):
        tree =  super(SignonAppCertRequest, self).build_element_tree()
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
            session_ticket=None, language=QBMS_LANGUAGE):
        self.app_id = app_id
        self.app_ver = app_ver
        self.application_login = application_login
        self.connection_ticket = connection_ticket
        self.session_ticket = session_ticket
        self.language = language

    def build_signon_msg_el(self):
        raise Exception("Not Implemented")

    def build_request(self, request_class, *args, **kwargs):
        kwargs['signon_msg_el'] = self.build_signon_msg_el()
        return request_class(*args, **kwargs)

    def perform_request(self, request):
        logging.debug("Sending Request:\n%s" % request.request_xml)
        return request

    def charge_credit_card(self, *args, **kwargs): 
        request = self.build_request(CustomerCreditCardChargeRequest, *args, **kwargs)
        return self.perform_request(request)


class QBMSHostedRequestor(QBMSRequestorBase):
    def __init__(self, session_ticket=None, *args, **kwargs):
        self.session_ticket = None
        super(QBMSHostedRequestor, self).__init__(*args, **kwargs)

    def build_signon_msg_el(self):
        if not self.session_ticket:
            self.signon()

        signon_ticket_rq = SignonTicketRq(session_ticket=self.session_ticket,
            language=self.language, 
            app_id=self.app_id, 
            app_ver=self.app_ver)
        return signon_ticket_rq.element

    def signon(self):
        logging.info('Performing Hosted Model Signon')
        request = SignonAppCertRequest(
            application_login = self.application_login,
            connection_ticket = self.connection_ticket
        )
        return self.perform_request(request)

    

        
