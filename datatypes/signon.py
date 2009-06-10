"""
Signon Ticket QuickBooks Data Types

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.base import QuickBooksAggregate, QuickBooksStrProperty, QuickBooksIntProperty
from pyqbms.datatypes.base import QuickBooksDateTimeProperty


class ClientDateTime(QuickBooksDateTimeProperty):
    pass

class SessionTicket(QuickBooksStrProperty):
    pass
    
class Language(QuickBooksStrProperty):
    pass

class AppID(QuickBooksIntProperty):
    pass

class AppVer(QuickBooksStrProperty):
    pass


class SignonTicketRq(QuickBooksAggregate):
    client_date_time    = ClientDateTime()
    session_ticket      = SessionTicket()
    language            = Language()
    app_id              = AppID()
    app_ver             = AppVer()


