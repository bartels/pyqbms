"""
QuickBooks API Request Encapsulation

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import pycurl, logging, traceback
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement
from pyqbms.datatypes.base import indent_tree


log = logging.getLogger(__name__)


try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


XML_VERSION = '1.0'


class QuickBooksRequestError(Exception):
    pass

class QuickBooksRequestBase(object):
    xml_version = XML_VERSION

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url', None)
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
            'Content-length: %i' % len(self.request_xml),
        ]

    def build_request_xml_headers(self):
        return '<?xml version="%s"?>' % self.xml_version

    def build_request_xml(self):
        self.element = self.build_element_tree()
        indent_tree(self.element)
        request_xml = ElementTree.tostring(self.element, 'utf-8')
        request_xml = self.build_request_xml_headers() + '\n' + request_xml 
        return request_xml

    def build_curl_rq(self):
        self.response_data_handle = StringIO.StringIO()
        curl_rq = pycurl.Curl()
        curl_rq.setopt(pycurl.URL, self.url)
        curl_rq.setopt(pycurl.WRITEFUNCTION, self.response_data_handle.write)
        curl_rq.setopt(pycurl.TIMEOUT, 500);
        curl_rq.setopt(pycurl.HTTPHEADER, self.build_headers())
        curl_rq.setopt(pycurl.POST, 1);
        curl_rq.setopt(pycurl.POSTFIELDS, self.request_xml);
        return curl_rq
        
    def perform(self):
        log.debug("Sending Request to: %s\n%s" % (self.url, self.request_xml))
        self.curl_rq = self.build_curl_rq()
        try:
            self.curl_rq.perform()
        except pycurl.error:
            raise QuickBooksRequestError, "Could not connect to host"
        finally:
            self.curl_rq.close()
            try:
                if hasattr(self.response_data_handle, 'read'): 
                    self.response_data = self.response_data_handle.getvalue()
                    log.debug(self.response_data)
                    self.response_data_handle.close()
            except:
                log.warning(traceback.format_exc())
        return self.parse_response()

    def parse_response(self):
        self.response_tree = ElementTree.parse(StringIO.StringIO(self.response_data))
        return self.response_tree

