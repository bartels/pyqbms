"""
QuickBooks Request and Response Data Type Definitions

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.base import QuickBooksAggregate
from pyqbms.datatypes.base import QuickBooksStrProperty, QuickBooksIntProperty


class StatusSeverity(QuickBooksStrProperty):
    def __init__(self, *args, **kwargs):
        kwargs['attribute'] = True
        kwargs['xpath'] = 'statusSeverity'
        super(StatusSeverity, self).__init__(*args, **kwargs)


class StatusMessage(QuickBooksStrProperty):
    def __init__(self, *args, **kwargs):
        kwargs['attribute'] = True
        kwargs['xpath'] = 'statusMessage'
        super(StatusMessage, self).__init__(*args, **kwargs)


class StatusCode(QuickBooksIntProperty):
    def __init__(self, *args, **kwargs):
        kwargs['attribute'] = True
        kwargs['xpath'] = 'statusCode'
        super(StatusCode, self).__init__(*args, **kwargs)


class QuickBooksResponseAggregate(QuickBooksAggregate):
    status_code = StatusCode()
    status_severity = StatusSeverity()
    status_message = StatusMessage()


class QuickBooksRequestAggregate(QuickBooksAggregate):
    pass
