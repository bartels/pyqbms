"""
Signon Ticket QuickBooks Data Types

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.base import QuickBooksAggregate, QuickBooksStrProperty, QuickBooksIntProperty
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms.datatypes.base import QuickBooksDateTimeProperty


class ClientDateTime(QuickBooksDateTimeProperty): pass

class ServerDateTime(QuickBooksDateTimeProperty): pass

class SessionTicket(QuickBooksStrProperty): pass
    
class Language(QuickBooksStrProperty): pass

class AppID(QuickBooksIntProperty): pass

class AppVer(QuickBooksStrProperty): pass

class ApplicationLogin(QuickBooksStrProperty): pass

class ConnectionTicket(QuickBooksStrProperty): pass


class SignonTicketRq(QuickBooksRequestAggregate):
    client_date_time    = ClientDateTime()
    session_ticket      = SessionTicket()
    language            = Language()
    app_id              = AppID()
    app_ver             = AppVer()

class SignonTicketRs(QuickBooksResponseAggregate):
    server_date_time    = ServerDateTime()
    session_ticket      = SessionTicket()


class SignonAppCertRq(QuickBooksRequestAggregate):
    client_date_time    = ClientDateTime()
    application_login   = ApplicationLogin()
    connection_ticket   = ConnectionTicket()


class SignonAppCertRs(QuickBooksResponseAggregate):
    server_date_time    = ServerDateTime()
    session_ticket      = SessionTicket()
    

class SignonDesktopRq(QuickBooksRequestAggregate):
    client_date_time    = ClientDateTime()
    application_login   = ApplicationLogin()
    connection_ticket   = ConnectionTicket()
    language            = Language()
    app_id              = AppID()
    app_ver             = AppVer()
    

class SignonDesktopRs(QuickBooksResponseAggregate):
    server_date_time    = ServerDateTime()
    session_ticket      = SessionTicket()
    language            = Language()
    app_id              = AppID()
    app_ver             = AppVer()


