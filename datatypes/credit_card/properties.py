"""
Credit Card QuickBooks Data Types

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.base import QuickBooksStrProperty, QuickBooksIntProperty
from pyqbms.datatypes.base import QuickBooksMonthProperty, QuickBooksYearProperty
from pyqbms.datatypes.base import QuickBooksDateTimeProperty, QuickBooksTimeStampProperty
from pyqbms.datatypes.base import QuickBooksAmtProperty, QuickBooksBoolProperty
from pyqbms.datatypes.base import QuickBooksEnumProperty


class TransRequestID(QuickBooksIntProperty):
    max_length = 50

class NameOnCard(QuickBooksStrProperty): 
    max_length = 30

class CreditCardNumber(QuickBooksStrProperty): 
    max_length = 30

class ExpirationMonth(QuickBooksMonthProperty): pass
class ExpirationYear(QuickBooksYearProperty): pass

class Track2Data(QuickBooksStrProperty):
    max_length = 39

class Amount(QuickBooksAmtProperty): pass
class SalesTaxAmount(QuickBooksAmtProperty): pass

class CreditCardAddress(QuickBooksIntProperty):
    max_length = 30

class CreditCardPostalCode(QuickBooksStrProperty):
    max_length = 9

class CommercialCardCode(QuickBooksStrProperty):
    max_length = 25

class CardSecurityCode(QuickBooksStrProperty):
    max_length = 4

class IsCardPresent(QuickBooksBoolProperty): pass
class IsECommerce(QuickBooksBoolProperty): pass
class IsRecurring(QuickBooksBoolProperty): pass
class ForceRefund(QuickBooksBoolProperty): pass
class ResultCode(QuickBooksIntProperty): pass
class ResultMessage(QuickBooksStrProperty): pass

class CreditCardTransID(QuickBooksStrProperty): 
    max_length = 12

class ClientTransID(QuickBooksStrProperty):
    max_length = 16

class MerchantAccountNumber(QuickBooksStrProperty):
    max_length = 16

class AuthorizationCode(QuickBooksStrProperty): 
    max_length = 6

class ReconBatchID(QuickBooksStrProperty):
    max_length = 84

class PaymentGroupingCode(QuickBooksIntProperty): pass
class PaymentStatus(QuickBooksStrProperty): pass
class TxnAuthorizationTime(QuickBooksDateTimeProperty): pass
class TxnAuthorizationStamp(QuickBooksTimeStampProperty): pass

class BatchID(QuickBooksStrProperty): 
    max_length = 4

class AVSStreet(QuickBooksEnumProperty): pass
class AVSZip(QuickBooksEnumProperty): pass
class CardSecurityCodeMatch(QuickBooksEnumProperty): pass

class PINBlock(QuickBooksStrProperty):
    max_length = 16

class SMID(QuickBooksStrProperty):
    max_length = 20

class CashBackAmount(QuickBooksAmtProperty): pass

class VoidOrRefundTxnType(QuickBooksEnumProperty): pass

class DebitCardTransID(QuickBooksStrProperty):
    max_length = 12

class NetworkName(QuickBooksStrProperty): pass
class NetworkNumber(QuickBooksStrProperty): pass
