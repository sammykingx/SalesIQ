from django.core.mail import get_connection, EmailMultiAlternatives
from anymail.exceptions import AnymailError, AnymailRequestsAPIError
from mailer.exceptions import (
    EmailSendError, EmailTimeoutError, EmailRateLimitedError,
    EmailServerError, EmailConfigurationError,
)
from .base import EmailProvider, EmailMessage

import logging

logger = logging.getLogger(__name__)


class ResendProvider(EmailProvider):
    backend_path = "anymail.backends.resend.EmailBackend"

    def send(self, message: EmailMessage) -> None:
        connection = get_connection(backend=self.backend_path)
        email = EmailMultiAlternatives(
            subject=message.subject,
            body=message.html_body,
            from_email=message.from_email,
            to=message.to,
            connection=connection,
        )
        email.attach_alternative(message.html_body, "text/html")
        for file_path in (message.attachments or []):
            email.attach_file(file_path)

        try:
            email.send()
        except AnymailRequestsAPIError as e:
            self._handle_api_error(e)
        except AnymailError as e:
            logger.error("Resend send failed (non-HTTP): %s", e)
            raise EmailSendError(str(e)) from e

    def _handle_api_error(self, e: AnymailRequestsAPIError) -> None:
        status_code = e.status_code
        raw_response = getattr(e.response, "text", None) if e.response else None

        logger.error("Resend API error status=%s message=%s response=%s", status_code, e, raw_response)

        if status_code is None:
            raise EmailTimeoutError(str(e), status_code=status_code, raw_response=raw_response) from e

        if status_code == 429:
            retry_after = e.response.headers.get("retry-after") if e.response else None
            raise EmailRateLimitedError(
                str(e), status_code=status_code, raw_response=raw_response,
                retry_after=int(retry_after) if retry_after else None,
            ) from e

        if status_code >= 500:
            raise EmailServerError(str(e), status_code=status_code, raw_response=raw_response) from e

        # 401, 422, 451, other 4xx ("developmental error")
        raise EmailConfigurationError(str(e), status_code=status_code, raw_response=raw_response) from e
    