class AccountsDomainException(Exception):
    """Base class for all accounts domains business logic errors."""
    def __init__(self, message: str,*, code: str, title: str, err_type: str = "warning"):
        self.message = message
        self.code = code
        self.title = title
        self.err_type = err_type
        super().__init__(self.message)
        
class DuplicateEmailError(AccountsDomainException):
    """Raised when attempting to register an email that already exists in the system."""
    def __init__(self, message: str = "An account with this email address already exists.", code: str = "DUPLICATE_EMAIL", title: str = "Email Already Taken", err_type: str = "warning"):
        super().__init__(message, code=code, title=title, err_type=err_type)


class InvalidTokenError(AccountsDomainException):
    """Raised when an account activation token is invalid, expired, or malformed."""
    def __init__(self, message: str = "The token is invalid or has expired.", code: str = "INVALID_OR_EXPIRED_TOKEN", title: str = "Invalid Token", err_type: str = "error"):
        super().__init__(message, code=code, title=title, err_type=err_type)


class UserNotFoundError(AccountsDomainException):
    """Raised when a requested user account cannot be found."""
    def __init__(self, message: str = "No account was found matching the provided details.", code: str = "USER_NOT_FOUND", title: str = "User Not Found", err_type: str = "warning"):
        super().__init__(message, code=code, title=title, err_type=err_type)
        
class MultipleBusinessNotAllowedError(AccountsDomainException):
    """Raised when a user attempts to register more than one business account."""
    def __init__(
        self, 
        message: str = "You can only register one business account at a time.", 
        code: str = "MULTIPLE_BUSINESS_NOT_ALLOWED", 
        title: str = "Business Already Exists", 
        err_type: str = "warning"
    ):
        super().__init__(message, code=code, title=title, err_type=err_type)
