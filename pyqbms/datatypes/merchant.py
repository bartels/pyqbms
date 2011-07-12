"""
Merchant QuickBooks Data Types

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.base import QuickBooksAggregate, QuickBooksAmtProperty, QuickBooksEnumProperty
from pyqbms.datatypes.credit_card import TransRequestID, BatchID

class ConvenienceFees(QuickBooksAmtProperty): pass
class CreditCardType(QuickBooksEnumProperty): pass


class MerchantAccountQueryRq(QuickBooksAggregate):
    pass


class MerchantAccountQueryRs(QuickBooksAggregate):
    convenience_fees    = ConvenienceFees()
    credit_card_types   = CreditCardType(occurs=(0,0))


class MerchantBatchCloseRq(QuickBooksAggregate):
    trans_request_id    = TransRequestID(occurs=1)
    batch_id            = BatchID() 


class MerchantBatchCloseRs(QuickBooksAggregate):
    pass


