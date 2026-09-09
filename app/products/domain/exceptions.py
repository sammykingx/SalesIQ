class ProductDomainException(Exception):
    """Base exception for all product domain errors."""
    def __init__(self, message: str, title: str = "Product Error", err_type: str = "info"):
        self.message = message
        self.title = title
        self.err_type = err_type
        super().__init__(self.message)


class ProductAlreadyExistsError(ProductDomainException):
    """Raised when trying to create a product with a name that already exists for the business."""
    def __init__(self, message: str = "A product with this name already exists for this business."):
        super().__init__(
            message=message,
            title="Product Already Exists",
            err_type="info"
        )


class ProductNotFoundError(ProductDomainException):
    """Raised when a requested product does not exist."""
    def __init__(self, message: str = "The requested product could not be found."):
        super().__init__(
            message=message,
            title="Product Not Found",
            err_type="info"
        )
        