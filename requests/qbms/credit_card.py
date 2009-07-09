"""
QuickBooks Merchant Services API Credit Card Requests

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.requests.qbms import QBMSXMLMsgsRequest
from pyqbms.datatypes.credit_card import CustomerCreditCardChargeRq, CustomerCreditCardChargeRs

class CustomerCreditCardChargeRequest(QBMSXMLMsgsRequest):
    rq_aggregate_type = CustomerCreditCardChargeRq
    rs_aggregate_type = CustomerCreditCardChargeRs


