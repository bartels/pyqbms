"""
Basic QuickBooks Data Type Definitions

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import logging, traceback
from decimal import Decimal
from pyqbms import ElementTree
Element = ElementTree.Element
SubElement = ElementTree.SubElement


def indent_tree(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent_tree(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class QuickBooksProperty(object):
    """
    Describes a property of a QuickBooksAggregate instance

    Defines logic for translating data back and forth from XML/Python
    """

    default_xpath = None

    def __init__(self, xpath=None, occurs=(0,1)):
        if occurs == 1:
            self.min_occurences = self.max_occurences = 1
        else:
            self.min_occurences = occurs[0] 
            self.max_occurences = occurs[1] 

        if not xpath:
            xpath = self.default_xpath
            if not xpath:
                xpath = self.__class__.__name__
        self.xpath = xpath

    def __get__(self, obj, objtype=None):
        if not hasattr(obj, 'element'):
            return self
        
        element = obj.element.find(self.xpath)
        return element

    def __set__(self, obj, value):
        element = obj.element.find(self.xpath)
        if element is None:

            element = SubElement(obj.element, self.xpath)
        element.text = value
        return element.text


class QuickBooksStrProperty(QuickBooksProperty):
    def __get__(self, *args, **kwargs):
        element = super(QuickBooksStrProperty, self).__get__(*args, **kwargs)
        if hasattr(element, 'text') and element.text:
            return element.text
        return None

    def __set__(self, obj, value):
        if not hasattr(obj, 'element'):
            return self
        element = obj.element.find(self.xpath)
        if element is None:
            element = SubElement(obj.element, self.xpath)
        element.text = unicode(value)
        return element.text


class QuickBooksIntProperty(QuickBooksStrProperty):
    def __get__(self, *args, **kwargs):
        result = super(QuickBooksStrProperty, self).__get__(*args, **kwargs)
        if result is None:
            return result
        try:
            return int(result)
        except:
            logging.warning(traceback.format_exc())
        return result


class QuickBooksBoolProperty(QuickBooksStrProperty):
    def __get__(self, *args, **kwargs):
        result = super(QuickBooksStrProperty, self).__get__(*args, **kwargs)
        if result is None:
            return result
        if hasattr(result, 'lower'):
            result = result.lower().strip()
            if result in ('false', 'no', 'fail'):
                return False
            elif result.lower() in ('true', 'yes', 'pass'):
                return True
        return None
    

class QuickBooksDateTimeProperty(QuickBooksStrProperty):
    pass
class QuickBooksTimeStampProperty(QuickBooksIntProperty):
    pass
class QuickBooksMonthProperty(QuickBooksIntProperty):
    pass
class QuickBooksYearProperty(QuickBooksIntProperty):
    pass

class QuickBooksEnumProperty(QuickBooksIntProperty):
    pass

class QuickBooksDecimalProperty(QuickBooksStrProperty):
    def __get__(self, *args, **kwargs):
        result = super(QuickBooksAmtProperty, self).__get__(*args, **kwargs)
        if result is None:
            return result
        try:
            return Decimal(result)
        except:
            logging.warning(traceback.format_exc())
        return result

class QuickBooksAmtProperty(QuickBooksDecimalProperty):
    pass


class QuickBooksAggregate(object):
    """
    ORM Around an element in QuickBooks XML with one or more QuickBooksProperty definitions
    """
    default_tag = None

    def __init__(self, element=None, tag=None, *args, **kwargs):
        if not tag:
            tag = self.default_tag
            if not tag:
                tag = self.__class__.__name__
        if not element:
            element = Element(tag)
        self.element = element
        self.init(*args, **kwargs)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return self.to_xml()

    def init(self, *args, **kwargs):
        pass

    def to_xml(self):
        indent_tree(self.element)
        return ElementTree.tostring(self.element, 'utf-8')
