class CustomerDomainException(Exception):
    """Base exception for all Customer domain errors."""
    def __init__(self, message: str, title: str = "Customer Error", err_type: str = "info"):
        self.message = message
        self.title = title
        self.err_type = err_type
        super().__init__(self.message)


class CustomerAlreadyExistsError(CustomerDomainException):
    """
    Raised when attempting to create a customer record that already exists 
    within the current business's customer base, preventing duplicates.
    """
    def __init__(
        self, 
        message: str = "This customer is already registered with your business. We've prevented a duplicate record from being created."
    ):
        super().__init__(
            message=message,
            title="Customer Already Exists",
            err_type="info"
        )
