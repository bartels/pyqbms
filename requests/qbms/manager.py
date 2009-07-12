"""
QuickBooks Merchant Services API Request Management

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
import logging, traceback, datetime
from pyqbms.datatypes.signon import SignonTicketRq
from pyqbms.requests.qbms.exceptions import QBMSException, QBMSSignonException
from pyqbms.requests.qbms.signon import SignonAppCertRequest, SignonDesktopRequest

QBMS_PTC_URL = "https://merchantaccount.ptc.quickbooks.com/j/AppGateway"
QBMS_LIVE_URL = "https://merchantaccount.quickbooks.com/j/AppGateway"
QBMS_CERT_PATH = 'qbms.pem'
QBMS_LANGUAGE = 'English'

QBMS_TEST_MODE = True

QBMS_APP_ID = ''
QBMS_APP_VERSION = ''



class QBMSManagerBase(object):
    def __init__(self, app_id, app_ver, application_login, connection_ticket, 
            session_ticket=None, language=QBMS_LANGUAGE, qbms_url=QBMS_PTC_URL):
        self.app_id = app_id
        self.app_ver = app_ver
        self.application_login = application_login
        self.connection_ticket = connection_ticket
        self.session_ticket = session_ticket
        self.language = language
        self.qbms_url = qbms_url

    def get_is_signed_on(self):
        if self.session_ticket:
            return True
        return False
    is_signed_on = property(get_is_signed_on)

    def build_signon_msg_el(self):
        if not self.is_signed_on:
            self.signon()

        signon_ticket_rq = SignonTicketRq(session_ticket=self.session_ticket,
            client_date_time=datetime.datetime.today())
        return signon_ticket_rq.element

    def signon(self):
        raise Exception("Not implemented")

    def build_request(self, request_class, *args, **kwargs):
        kwargs['signon_msg_el'] = self.build_signon_msg_el()
        if not 'url' in kwargs:
            kwargs['url'] = self.qbms_url
        return request_class(*args, **kwargs)

    def perform_request(self, request):
        request.perform()
        return request

    def do_request(self, request_class, *args, **kwargs):
        request = self.build_request(request_class, *args, **kwargs)
        self.perform_request(request)
        return request.response

    def credit_card_auth(self, *args, **kwargs):
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardAuthRequest
        return self.do_request(CustomerCreditCardAuthRequest, *args, **kwargs)

    def credit_card_voice_auth(self, *args, **kwargs):
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardVoiceAuthRequest
        return self.do_request(CustomerCreditCardVoiceAuthRequest, *args, **kwargs)

    def credit_card_capture(self, *args, **kwargs):
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardCaptureRequest
        return self.do_request(CustomerCreditCardCaptureRequest, *args, **kwargs)

    def credit_card_charge(self, *args, **kwargs): 
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardChargeRequest
        return self.do_request(CustomerCreditCardChargeRequest, *args, **kwargs)

    def credit_card_refund(self, *args, **kwargs): 
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardRefundRequest
        return self.do_request(CustomerCreditCardRefundRequest, *args, **kwargs)

    def credit_card_txn_void(self, *args, **kwargs): 
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardTxnVoidRequest
        return self.do_request(CustomerCreditCardTxnVoidRequest, *args, **kwargs)

    def credit_card_txn_void_or_refund(self, *args, **kwargs): 
        from pyqbms.requests.qbms.credit_card import CustomerCreditCardTxnVoidOrRefundRequest
        return self.do_request(CustomerCreditCardTxnVoidOrRefundRequest, *args, **kwargs)

    def debit_card_charge(self, *args, **kwargs): 
        from pyqbms.requests.qbms.credit_card import CustomerDebitCardChargeRequest
        return self.do_request(CustomerDebitCardChargeRequest, *args, **kwargs)


class QBMSDesktopManager(QBMSManagerBase):
    def signon(self):
        logging.info('Performing Desktop Signon')
        request = SignonDesktopRequest(
            url = self.qbms_url,
            client_date_time=datetime.datetime.today(),
            application_login = self.application_login,
            # app_id = self.app_id,
            # app_ver = self.app_ver,
            # language = self.language,
            connection_ticket = self.connection_ticket
        )
        self.perform_request(request)
        self.session_ticket = request.response.session_ticket
        logging.info('Successful Desktop Signon')
        return request.response


class QBMSHostedManager(QBMSManagerBase):
    def signon(self):
        logging.info('Performing Hosted Model Signon')
        request = SignonAppCertRequest(
            url = self.qbms_url,
            client_date_time=datetime.datetime.today(),
            application_login = self.application_login,
            # app_id = self.app_id,
            # app_ver = self.app_ver,
            # language = self.language,
            connection_ticket = self.connection_ticket
        )
        self.perform_request(request)
        return request

    def do_request(self, *args, **kwargs):
        try:
            return super(QBMSHostedManager, self).do_request(*args, **kwargs)
        except QBMSSignonException, e:
            logging.warning(traceback.format_exc())
            self.session_ticket = None
            self.signon()
            return super(QBMSHostedManager, self).do_request(*args, **kwargs)
              

    

        

