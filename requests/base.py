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
from pyqbms.datatypes.base import indent_tree



try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


XML_VERSION = '1.0'


class QuickBooksRequestBase(object):
    xml_version = XML_VERSION

    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)
        self.request_xml = self.build_request_xml()

    def __repr__(self):
        return self.request_xml

    def init(self, *args, **kwargs):
        pass

    def build_element_tree(self):
        raise Exception('Not Implemented')

    def build_headers(self):
        return [
            'Content-length: ' + len(self.request_xml),
        ]

    def build_request_xml_headers(self):
        return '<?xml version="%s"?>' % self.xml_version

    def build_request_xml(self):
        self.element = self.build_element_tree()
        indent_tree(self.element)
        request_xml = ElementTree.tostring(self.element, 'utf-8')
        request_xml = self.build_request_xml_headers() + '\n' + request_xml 
        return request_xml

    def build_request(self):
        self.response_data_handle = StringIO.StringIO()
        request = pycurl.Curl()
        request.setopt(pycurl.URL, self.url)
        request.setopt(pycurl.WRITEFUNCTION, self.response_data_handle.write)
        request.setopt(pycurl.TIMEOUT, 500);
        request.setopt(pycurl.HTTPHEADER, self.build_headers())
        request.setopt(pycurl.POST, 1);
        request.setopt(pycurl.POSTFIELDS, self.request_xml);

        return request
        
    def perform(self):
        self.request = self.build_request()


