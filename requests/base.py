"""
QuickBooks API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement

QBMS_URL = "https://merchantaccount.ptc.quickbooks.com/j/AppGateway"
QBMS_CERT_PATH = 'qbms.pem'


try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
class QBMSRequest(object):
    def __init__(self, *args, **kwargs):
        self.response_data_handle = StringIO.StringIO()
        self.init(*args, **kwargs)
        self.request_xml = self.build_request_xml()

    def __repr__(self):
        return self.request_xml

    def init(self, *args, **kwargs):
        pass

    def build_element_tree(self):
        qbxml = Element('QBXML')
        return qbxml

    def build_headers(self):
        return [
            'Content-type: application/x-qbmsxml',
            'Content-length: ' + len(self.request_xml)
        ]

    def build_request_xml(self):
        self.element = self.build_element_tree()
        return ElementTree.tostring(self.element, 'utf-8')

    def build_request(self):
        request = pycurl.Curl()
        request.setopt(pycurl.URL, self.url)
        request.setopt(pycurl.WRITEFUNCTION, self.response_data_handle.write)
        request.setopt(pycurl.TIMEOUT, 500);
        request.setopt(pycurl.HTTPHEADER, self.build_headers())
        request.setopt(pycurl.POST, 1);
        request.setopt(pycurl.POSTFIELDS, self.request_xml);
        request.setopt(pycurl.SSLCERT, QBMS_CERT_PATH);

        return request
        
    def perform(self):
        self.request = self.build_request()

