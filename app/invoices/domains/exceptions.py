class InvoiceDomainException(Exception):
    """Base class for all invoice domain business logic errors."""

    def __init__(self, message: str, *, code: str, title: str, err_type: str = "error"):
        self.message = message
        self.code = code
        self.title = title
        self.err_type = err_type
        super().__init__(self.message)

class InvoiceIdentifierCollisionError(InvoiceDomainException):
    """
    Raised when a unique display_id/slug could not be produced —
    either the retry loop exhausted its attempts, or a concurrent
    write collided with the candidate at insert time.
    """
    def __init__(
        self,
        message: str = "We couldn't generate a unique invoice ID. Please try again.",
        *,
        code: str = "invoice_identifier_collision",
        title: str = "Invoice Creation Failed",
        err_type: str = "error",
    ):
        super().__init__(message, code=code, title=title, err_type=err_type)

class InvalidInvoiceDataError(InvoiceDomainException):
    """
    Raised when a value on the invoice or a line item can't be persisted
    as-is — e.g. exceeds a field's max_digits, or fails a DB-level
    constraint on the data itself rather than on identity/uniqueness.
    """
    def __init__(
        self,
        message: str = "One of the values on this sale is too large or invalid to process.",
        *,
        code: str = "invoice_invalid_data",
        title: str = "Sale Not Saved",
        err_type: str = "error",
    ):
        super().__init__(message, code=code, title=title, err_type=err_type)

class InvoiceWriteFailedError(InvoiceDomainException):
    """
    Raised for structural write failures that aren't about identifier
    collisions or bad values — e.g. a foreign key referencing a business,
    customer, or product that no longer exists.
    """
    def __init__(
        self,
        message: str = "This sale could not be saved because related data was missing or changed.",
        *,
        code: str = "invoice_write_failed",
        title: str = "Sale Not Saved",
        err_type: str = "error",
    ):
        super().__init__(message, code=code, title=title, err_type=err_type)

class InvoiceServiceUnavailableError(InvoiceDomainException):
    """
    Raised for transient DB failures (connection drop, deadlock, timeout)
    where retrying the same request is likely to succeed.
    """
    def __init__(
        self,
        message: str = "A temporary issue prevented this sale from saving. Please try again.",
        *,
        code: str = "invoice_service_unavailable",
        title: str = "Sale Not Saved",
        err_type: str = "warning",
    ):
        super().__init__(message, code=code, title=title, err_type=err_type)
