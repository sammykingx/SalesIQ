class InvoiceDomainException(Exception):
    """Base class for all invoice domains business logic errors."""
    
    def __init__(self, message: str,*, code: str, title: str, err_type: str = "warning"):
        self.message = message
        self.code = code
        self.title = title
        self.err_type = err_type
        super().__init__(self.message)
