"""
QuickBooks Merchant Services API Credit Card Requests

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.requests.qbms import QBMSXMLMsgsRequest
from pyqbms.datatypes.credit_card import CustomerCreditCardAuthRq, CustomerCreditCardAuthRs
from pyqbms.datatypes.credit_card import CustomerCreditCardVoiceAuthRq, CustomerCreditCardVoiceAuthRs
from pyqbms.datatypes.credit_card import CustomerCreditCardCaptureRq, CustomerCreditCardCaptureRs
from pyqbms.datatypes.credit_card import CustomerCreditCardChargeRq, CustomerCreditCardChargeRs
from pyqbms.datatypes.credit_card import CustomerCreditCardRefundRq, CustomerCreditCardRefundRs
from pyqbms.datatypes.credit_card import CustomerCreditCardTxnVoidRq, CustomerCreditCardTxnVoidRs
from pyqbms.datatypes.credit_card import CustomerCreditCardTxnVoidOrRefundRq, CustomerCreditCardTxnVoidOrRefundRs
from pyqbms.datatypes.credit_card import CustomerDebitCardChargeRq, CustomerDebitCardChargeRs


class CustomerCreditCardAuthRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardAuthRq
    rs_aggregate_type = CustomerCreditCardAuthRs

class CustomerCreditCardVoiceAuthRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardVoiceAuthRq
    rs_aggregate_type = CustomerCreditCardVoiceAuthRs

class CustomerCreditCardCaptureRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardCaptureRq
    rs_aggregate_type = CustomerCreditCardCaptureRs

class CustomerCreditCardChargeRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardChargeRq
    rs_aggregate_type = CustomerCreditCardChargeRs

class CustomerCreditCardRefundRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardRefundRq
    rs_aggregate_type = CustomerCreditCardRefundRs

class CustomerCreditCardTxnVoidRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardTxnVoidRq
    rs_aggregate_type = CustomerCreditCardTxnVoidRs

class CustomerCreditCardTxnVoidOrRefundRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardTxnVoidOrRefundRq
    rs_aggregate_type = CustomerCreditCardTxnVoidOrRefundRs

class CustomerDebitCardChargeRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerDebitCardChargeRq
    rs_aggregate_type = CustomerDebitCardChargeRs


