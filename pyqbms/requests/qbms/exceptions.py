"""
QuickBooks Merchant Services API Request Exceptions

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""


class QBMSErrorType(type):
    """Metaclass that maintains mapping of status code to exception classes"""
    status_code_map = {}

    def __new__(mcs, name, bases, attrs):
        super_new = super(QBMSErrorType, mcs).__new__
        new_class = super_new(mcs, name, bases, attrs)
        if hasattr(new_class, 'status_code'):
            mcs.status_code_map[new_class.status_code] = new_class
        return new_class

    @classmethod
    def from_rs(cls, response):
        """Return an Exception of the appropriate type based on the status_code of a rs aggregate"""
        message = None
        status_code = None

        if hasattr(response, 'status_message'):
            message = response.status_message

        if hasattr(response, 'status_code'):
            status_code = response.status_code

        exc_class = cls.status_code_map.get(status_code, Exception)
        return exc_class(message)


class QBMSException(Exception):
    """Base Exception class for all errors returned by the QBMS API servers"""
    __metaclass__ = QBMSErrorType
    status_code = None

    def __init__(self, message):
        self.message = message

    def _get_message(self):
        return self._message
    def _set_message(self, message):
        self._message = message
    message = property(_get_message, _set_message)


class QBMSGatewayException(QBMSException):
    """Base Exception class for any QBMS gateway related errors"""

class QBMSSignonException(QBMSException):
    """Base Exception class for any errors that can be potentially fixed with a new signon"""

class QBMSAuthenticationFailed(QBMSSignonException):
    status_code = 2000

class QBMSUnauthorizedException(QBMSException):
    status_code = 2010

class QBMSSessionAuthenticationRequired(QBMSSignonException):
    status_code = 2020

class QBMSUnsupportedSignonVersion(QBMSException):
    status_code = 2030

class QBMSInternalError(QBMSException):
    status_code = 2040

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

class QBMSCardValidationException(QBMSDataValidationException):
    status_code = 10409

class QBMSBatchIDMissingException(QBMSException):
    status_code = 10413

class QBMSGeneralGatewayException(QBMSGatewayException):
    status_code = 10500

class QBMSGeneralSystemException(QBMSException):
    status_code = 10501
