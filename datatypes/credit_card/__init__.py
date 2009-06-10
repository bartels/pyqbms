"""
QuickBooks Credit Card Data Types

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from pyqbms.datatypes.request import QuickBooksResponseAggregate, QuickBooksRequestAggregate
from pyqbms.datatypes.credit_card import properties as props


class CustomerCreditCardAuthRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)

    credit_card_number      = props.CreditCardNumber()
    expiration_month        = props.ExpirationMonth()
    expiration_year         = props.ExpirationYear()

    is_card_present         = props.IsCardPresent()
    is_ecommerce            = props.IsECommerce()
    is_recurring            = props.IsRecurring()

    track2data              = props.Track2Data()

    amount                  = props.Amount(occurs=1)

    name_on_card            = props.NameOnCard()
    credit_card_address     = props.CreditCardAddress()
    credit_card_postal_code = props.CreditCardPostalCode()
    commercial_card_code    = props.CommercialCardCode()
    sales_tax_amount        = props.SalesTaxAmount()
    card_security_code      = props.CardSecurityCode()

    batch_id                = props.BatchID()


class CustomerCreditCardAuthRs(QuickBooksResponseAggregate):
    credit_card_trans_id        = props.CreditCardTransID()
    authorization_code          = props.AuthorizationCode()
    avs_street                  = props.AVSStreet()
    avs_zip                     = props.AVSZip()
    card_security_code_match    = props.CardSecurityCodeMatch()
    client_trans_id             = props.ClientTransID() 


class CustomerCreditCardVoiceAuthRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)

    credit_card_number      = props.CreditCardNumber()
    expiration_month        = props.ExpirationMonth()
    expiration_year         = props.ExpirationYear()

    is_card_present         = props.IsCardPresent()
    is_ecommerce            = props.IsECommerce()

    track2data              = props.Track2Data()

    amount                  = props.Amount(occurs=1)
    authorization_code      = props.AuthorizationCode(occurs=1)
    commercial_card_code    = props.CommercialCardCode()
    sales_tax_amount        = props.SalesTaxAmount()
    batch_id                = props.BatchID()


class CustomerCreditCardVoiceAuthRs(QuickBooksResponseAggregate):
    credit_card_trans_id    = props.CreditCardTransID()
    authorization_code      = props.AuthorizationCode()
    merchant_account_number = props.MerchantAccountNumber()
    recon_batch_id          = props.ReconBatchID()
    payment_grouping_code   = props.PaymentGroupingCode()
    payment_status          = props.PaymentStatus()
    txn_authorization_time  = props.TxnAuthorizationTime()
    txn_authorization_stamp = props.TxnAuthorizationStamp()
    client_trans_id         = props.ClientTransID()


class CustomerCreditCardCaptureRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)
    credit_card_trans_id    = props.CreditCardTransID(occurs=1)
    amount                  = props.Amount()


class CustomerCreditCardCaptureRs(QuickBooksResponseAggregate):
    credit_card_trans_id    = props.CreditCardTransID()
    authorization_code      = props.AuthorizationCode()
    merchant_account_number = props.MerchantAccountNumber()
    recon_batch_id          = props.ReconBatchID()
    payment_grouping_code   = props.PaymentGroupingCode()
    payment_status          = props.PaymentStatus()
    txn_authorization_time  = props.TxnAuthorizationTime()
    txn_authorization_stamp = props.TxnAuthorizationStamp()
    client_trans_id         = props.ClientTransID()
    

class CustomerCreditCardChargeRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)

    credit_card_number      = props.CreditCardNumber()
    expiration_month        = props.ExpirationMonth()
    expiration_year         = props.ExpirationYear()

    is_card_present         = props.IsCardPresent()
    is_ecommerce            = props.IsECommerce()
    is_recurring            = props.IsRecurring()

    track2data              = props.Track2Data()

    amount                  = props.Amount()
    name_on_card            = props.NameOnCard()
    credit_card_address     = props.CreditCardAddress()
    credit_card_postal_code = props.CreditCardPostalCode()
    commercial_card_code    = props.CommercialCardCode()
    sales_tax_amount        = props.SalesTaxAmount()
    card_security_code      = props.CardSecurityCode()


class CustomerCreditCardChargeRs(QuickBooksResponseAggregate):
    credit_card_trans_id        = props.CreditCardTransID()
    authorization_code          = props.AuthorizationCode()
    avs_street                  = props.AVSStreet()
    avs_zip                     = props.AVSZip()
    card_security_code_match    = props.CardSecurityCodeMatch()
    merchant_account_number     = props.MerchantAccountNumber()
    recon_batch_id              = props.ReconBatchID()
    payment_grouping_code       = props.PaymentGroupingCode()
    payment_status              = props.PaymentStatus()
    txn_authorization_time      = props.TxnAuthorizationTime()
    txn_authorization_stamp     = props.TxnAuthorizationStamp()
    client_trans_id             = props.ClientTransID()


class CustomerCreditCardRefundRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)

    credit_card_number      = props.CreditCardNumber()
    expiration_month        = props.ExpirationMonth()
    expiration_year         = props.ExpirationYear()

    is_card_present         = props.IsCardPresent()
    is_ecommerce            = props.IsECommerce()

    track2data              = props.Track2Data()

    amount                  = props.Amount(occurs=1)

    name_on_card            = props.NameOnCard()
    commercial_card_code    = props.CommercialCardCode()
    sales_tax_amount        = props.SalesTaxAmount()
    batch_id                = props.BatchID()


class CustomerCreditCardRefundRs(QuickBooksResponseAggregate):
    credit_card_trans_id    = props.CreditCardTransID()
    merchant_account_number = props.MerchantAccountNumber()
    recon_batch_id          = props.ReconBatchID()
    payment_grouping_code   = props.PaymentGroupingCode()
    payment_status          = props.PaymentStatus()
    txn_authorization_time  = props.TxnAuthorizationTime()
    txn_authorization_stamp = props.TxnAuthorizationStamp()
    client_trans_id         = props.ClientTransID()


class CustomerCreditCardTxnVoidRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)
    credit_card_trans_id    = props.CreditCardTransID(occurs=1)
    client_trans_id         = props.ClientTransID()
    batch_id                = props.BatchID()


class CustomerCreditCardTxnVoidRs(QuickBooksResponseAggregate):
    credit_card_trans_id    = props.CreditCardTransID()
    client_trans_id         = props.ClientTransID()


class CustomerCreditCardTxnVoidOrRefundRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)
    credit_card_trans_id    = props.CreditCardTransID(occurs=1)
    client_trans_id         = props.ClientTransID()
    amount                  = props.Amount()
    commercial_card_code    = props.CommercialCardCode()
    sales_tax_amount        = props.SalesTaxAmount()
    force_refund            = props.ForceRefund()
    batch_id                = props.BatchID()


class CustomerCreditCardTxnVoidOrRefundRs(QuickBooksResponseAggregate):
    credit_card_trans_id    = props.CreditCardTransID(occurs=1)
    client_trans_id         = props.ClientTransID()
    void_or_refund_txn_type = props.VoidOrRefundTxnType()
    merchant_account_number = props.MerchantAccountNumber()
    recon_batch_id          = props.ReconBatchID()
    payment_grouping_code   = props.PaymentGroupingCode()
    payment_status          = props.PaymentStatus()
    txn_authorization_time  = props.TxnAuthorizationTime()
    txn_authorization_stamp = props.TxnAuthorizationStamp()


class CustomerDebitCardChargeRq(QuickBooksRequestAggregate):
    trans_request_id        = props.TransRequestID(occurs=1)
    track2data              = props.Track2Data(occurs=1)
    pin_block               = props.PINBlock(occurs=1)
    smid                    = props.SMID(occurs=1)
    amount                  = props.Amount(occurs=1)
    name_on_card            = props.NameOnCard()
    cash_back_amount        = props.CashBackAmount()
    batch_id                = props.BatchID()


class CustomerDebitCardChargeRs(QuickBooksResponseAggregate):
    debit_card_trans_id     = props.DebitCardTransID()
    authorization_code      = props.AuthorizationCode()
    network_name            = props.NetworkName()
    network_number          = props.NetworkNumber()
    merchant_account_number = props.MerchantAccountNumber()
    recon_batch_id          = props.ReconBatchID()
    payment_grouping_code   = props.PaymentGroupingCode()
    payment_status          = props.PaymentStatus()
    txn_authorization_time  = props.TxnAuthorizationTime()
    txn_authorization_stamp = props.TxnAuthorizationStamp()
    client_trans_id         = props.ClientTransID()



