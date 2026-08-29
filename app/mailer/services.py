# mailer/services.py
from django.conf import settings
from django.utils.html import strip_tags
from typing import Union
from .providers.base import EmailMessage, Providers, EmailProvider
from .providers.resend import ResendProvider
from .exceptions import EmailSendError
# from .models import EmailLog


class AppMailerService:
    _PROVIDERS: dict[str, EmailProvider] = {
        Providers.RESEND: ResendProvider(),
        # Providers.SMTP: SMTPProvider(),
    }

    def __init__(self, provider: Providers) -> None:
        # provider = provider or settings.DEFAULT_EMAIL_PROVIDER
        try:
            self.mail_client = self._PROVIDERS[provider]
        except KeyError:
            raise ValueError(f"No provider registered for '{provider}'")
        self.provider_name = provider
        self.message: Union[EmailMessage, None] = None

    def prepare_message(
        self, *, subject: str, html_msg: str, recipients: Union[list[str], str],
        from_email: Union[str, None] = None, attachments: Union[list[str], None] = None,
    ) -> "AppMailerService":
        self.message = EmailMessage(
            to=recipients if isinstance(recipients, list) else [recipients],
            subject=subject,
            html_body=html_msg,
            text_body=strip_tags(html_msg),
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            attachments=attachments,
        )
        return self

    def send_email(self) -> None:
        if self.message is None:
            raise ValueError("Call prepare_message() before send_email()")

        self.mail_client.send(self.message)
            