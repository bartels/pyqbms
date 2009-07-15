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

    creation_counter = 0

    def __init__(self, xpath=None, occurs=(0,1), attribute=False):
        self.creation_counter = QuickBooksProperty.creation_counter
        QuickBooksProperty.creation_counter += 1

        if occurs == 1:
            self.min_occurences = self.max_occurences = 1
        else:
            self.min_occurences = occurs[0] 
            self.max_occurences = occurs[1] 

        self.is_attribute = attribute
        if not xpath:
            xpath = self.default_xpath
            if not xpath:
                xpath = self.__class__.__name__
        self.xpath = xpath

    def __cmp__(self, other):
        return cmp(self.creation_counter, other.creation_counter)

    def __get__(self, obj, objtype=None):
        if not hasattr(obj, 'element'):
            return self
        
        if self.is_attribute:
            result =  obj.element.attrib.get(self.xpath, None)
            return result
        else:
            element = obj.element.find(self.xpath)
            return element

    def __set__(self, obj, value):
        if self.is_attribute:
            obj.element.set(self.xpath, value)
            return value
        else:
            element = obj.element.find(self.xpath)
            if element is None:
                element = SubElement(obj.element, self.xpath)
            element.text = value
            return element.text


class QuickBooksStrProperty(QuickBooksProperty):
    def __get__(self, *args, **kwargs):
        if self.is_attribute:
            return super(QuickBooksStrProperty, self).__get__(*args, **kwargs)
        element = super(QuickBooksStrProperty, self).__get__(*args, **kwargs)
        if hasattr(element, 'text') and element.text:
            return element.text
        return None

    def __set__(self, obj, value):
        if self.is_attribute:
            return super(QuickBooksStrProperty, self).__set__(obj, value)
        if not hasattr(obj, 'element'):
            return self
        element = obj.element.find(self.xpath)
        if element is None:
            element = SubElement(obj.element, self.xpath)
        element.text = unicode(value)
        return element.text


class QuickBooksIntProperty(QuickBooksStrProperty):
    def __get__(self, *args, **kwargs):
        result = super(QuickBooksIntProperty, self).__get__(*args, **kwargs)
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
    datetime_format = "%Y-%m-%dT%H:%M:%S"

    def __set__(self, obj, value):
        if hasattr(value, 'strftime'):
            value = value.strftime(self.datetime_format)
        return super(QuickBooksDateTimeProperty, self).__set__(obj, value)

class QuickBooksTimeStampProperty(QuickBooksIntProperty): pass
class QuickBooksMonthProperty(QuickBooksIntProperty): pass
class QuickBooksYearProperty(QuickBooksIntProperty): pass
class QuickBooksEnumProperty(QuickBooksStrProperty): pass

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


class QuickBooksAggregateMeta(type):
    def __new__(mcs, name, bases, attrs):
        super_new = super(QuickBooksAggregateMeta, mcs).__new__
        new_class = super_new(mcs, name, bases, {})

        setattr(new_class, 'qb_property_list', [])
        
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        new_class.qb_property_list.sort()

        return new_class

    def add_to_class(mcs, name, value):
        if isinstance(value, QuickBooksProperty):
            value.prop_name = name
            mcs.qb_property_list.append(value)
        setattr(mcs, name, value)


class QuickBooksAggregate(object):
    """
    ORM Around an element in QuickBooks XML with one or more QuickBooksProperty definitions
    """
    __metaclass__ = QuickBooksAggregateMeta

    default_tag = None

    def __init__(self, element=None, tag=None, *args, **kwargs):
        if not tag:
            tag = self.default_tag
            if not tag:
                tag = self.__class__.__name__
        if element is None:
            element = Element(tag)
        self.element = element
        self.init(*args, **kwargs)


        for property in self.qb_property_list:
            if property.prop_name in kwargs:
                setattr(self, property.prop_name, kwargs[property.prop_name])
            elif property.min_occurences > 0:
                setattr(self, property.prop_name, '')

    def __repr__(self):
        return self.to_xml()

    def init(self, *args, **kwargs):
        pass

    def to_xml(self):
        indent_tree(self.element)
        return ElementTree.tostring(self.element, 'utf-8')
