"""
QuickBooks Merchant Services API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl
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
    def build_element_tree(self):
        tree =  super(QBMSXMLMsgsRequest, self).build_element_tree()
        self.signon_msgs_rq_el.append(self.signon_ticket_rq.element)
        self.qbms_xml_msgs_rq_el = SubElement(self.qbmsxml_el, 'QBMSXMLMsgsRq')
        self.qbms_xml_msgs_rq_el.append(self.rq_aggregate.element)
        return tree

    def init(self, session_ticket, *args, **kwargs):
        self.signon_ticket_rq = SignonTicketRq(session_ticket=session_ticket,
            language=kwargs.get('language', QBMS_LANGUAGE), 
            app_id=kwargs.get('app_id', QBMS_APP_ID), 
            app_ver=kwargs.get('app_ver', QBMS_APP_VERSION))
        super(QBMSXMLMsgsRequest, self).init(*args, **kwargs)


class CustomerCreditCardChargeRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardChargeRq
    rs_aggregate_type = CustomerCreditCardChargeRs



