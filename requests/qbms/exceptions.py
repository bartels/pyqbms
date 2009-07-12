"""
QuickBooks Merchant Services API Request Exceptions

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""


class QBMSException(Exception):
    status_code = None

class QBMSGatewayException(QBMSException): pass

class QBMSSignonException(QBMSException): pass

class QBMSGatewayCommunicationException(QBMSGatewayException):
    status_code = 10200

class QBMSGatewayLoginException(QBMSGatewayException):
    status_code = 10201
    
class QBMSAccountValidationException(QBMSException):
    status_code = 10202

class QBMSDataValidationException(QBMSException):
    status_code = 10305

class QBMSAmountConversionException(QBMSDataValidationException):
    status_code = 10300

class QBMSInvalidCreditCardNumber(QBMSException):
    status_code = 10301

class QBMSDateValidationException(QBMSDataValidationException):
    status_code = 10302

class QBMSRequiredElementEmptyException(QBMSDataValidationException):
    status_code = 10303

class QBMSStringTooLong(QBMSDataValidationException):
    status_code = 10304

class QBMSBooleanValidationException(QBMSDataValidationException):
    status_code = 10306

class QBMSStringTooShort(QBMSDataValidationException):
    status_code = 10307

class QBMSExceededMaximumRequestsPerPostException(QBMSException):
    status_code = 10308

class QBMSInvalidFieldFormatException(QBMSDataValidationException):
    status_code = 10309

class QBMSInvalidFieldException(QBMSDataValidationException):
    status_code = 10312

class QBMSInvalidAggregateException(QBMSDataValidationException):
    status_code = 10313

class QBMSInsufficientFundsException(QBMSException):
    status_code = 10400

class QBMSTransactionRequestDeclined(QBMSException):
    status_code = 10401

class QBMSMerchantAccountDoesntSupportCardType(QBMSException):
    status_code = 10402

class QBMSMerchantAccountInfoUnrecognized(QBMSException):
    status_code = 10403

class QBMSVoiceAuthRequired(QBMSTransactionRequestDeclined):
    status_code = 10404

class QBMSTransactionVoidException(QBMSException):
    status_code = 10405

class QBMSCaptureException(QBMSException):
    status_code = 10406

class QBMSSalesCapExceeded(QBMSException):
    status_code = 10407

class QBMSInvalidDataFormatException(QBMSDataValidationException):
    status_code = 10408

class QBMSCardValidationException(QBMSException):
    status_code = 10409

class QBMSBatchIDMissingException(QBMSException):
    status_code = 10413

class QBMSGeneralGatewayException(QBMSGatewayException):
    status_code = 10500

class QBMSGeneralSystemException(QBMSException):
    status_code = 10501


