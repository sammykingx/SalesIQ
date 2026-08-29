from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmailMessage:
    to: list[str]
    subject: str
    html_body: str
    text_body: str
    from_email: str
    attachments: list[tuple[str, bytes, str]] | None = None  # (filename, bytes, mimetype)

class EmailProvider(ABC):
    @abstractmethod
    def send(self, message: EmailMessage) -> None:
        """Raise EmailSendError on failure."""
