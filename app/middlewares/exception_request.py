import contextvars


_CURRENT_REQUEST = contextvars.ContextVar("CURRENT_REQUEST", default=None)


class ExceptionRequestMiddleware:
    """Middleware that stores the active HTTP request in a context variable.

    This makes the current request accessible globally within the current
    execution context (such as custom logging formatters, error handlers,
    or exception tracebacks) for enhanced debugging.

    Placement:
        Place this as early as possible in your `MIDDLEWARE` settings (ideally 
        before `AuthenticationMiddleware`) so that the request context is 
        available during authentication and subsequent request processing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        active_request = _CURRENT_REQUEST.set(request)
        try:
            return self.get_response(request)
        finally:
            _CURRENT_REQUEST.reset(active_request)
