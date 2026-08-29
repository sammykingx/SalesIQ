from django.core.mail import EmailMultiAlternatives
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Union


class Providers(StrEnum):
    RESEND = "resend"
    SERVER_SMTP = "server_smtp"

@dataclass
class EmailMessage:
    """Data container representing the payload for an outgoing email.

    This class acts as a structured schema to hold all necessary email components 
    before they are mapped into a Django EmailMultiAlternatives object for delivery.

    Attributes:
        to (list[str]): A list of recipient email addresses.
        subject (str): The subject line of the email.
        html_body (str): The HTML-formatted version of the email content.
        text_body (str): The plain-text fallback version of the email content.
        from_email (str): The sender's email address (and optional display name).
        attachments (Union[list[str], None]): Optional list of absolute file 
            paths to attach. Defaults to None.
    """
    to: list[str]
    subject: str
    html_body: str
    from_email: str
    text_body: Union[str, None] = None
    attachments: Union[list[str], None] = None

class EmailProvider(ABC):
    @abstractmethod
    def send(self, message: EmailMessage) -> None:
        """Send the message. Must raise EmailSendError (or a subclass) on any failure —
        nothing above this layer should ever see a provider-specific exception."""
