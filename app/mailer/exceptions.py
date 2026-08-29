class EmailSendError(Exception):
    """Base for any failed send. Carries status_code/raw_response so callers
    (and logs) don't need to re-inspect the original provider exception.
    """
    
    user_message =  "Success! However, the email failed to send."
    
    def __init__(self, message: str, *, status_code: int | None = None, raw_response: str | None = None):
        self.status_code = status_code
        self.raw_response = raw_response
        super().__init__(message)


class EmailTimeoutError(EmailSendError):
    """No response received at all — connection/read timeout, DNS failure. Safe to retry."""
    
    user_message = "Success! However, the email is running a bit late"


class EmailRateLimitedError(EmailSendError):
    """429 — Exceeding resend's quota, ideally after `retry_after` seconds."""
    
    user_message = "Succeess! However, email is queued and on its way."
    
    def __init__(self, message: str, *, status_code=None, raw_response=None, retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(message, status_code=status_code, raw_response=raw_response)


class EmailServerError(EmailSendError):
    """5xx — Resend-side outage/maintenance. Transient, safe to retry."""
    user_message = "Email service currently unavailable"


class EmailConfigurationError(EmailSendError):
    """4xx other than 429 — bad API key, malformed from/to, rejected content.
    This is a code/config bug, not a transient failure — retrying won't fix it."""