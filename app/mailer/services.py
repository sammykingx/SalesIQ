# mailer/services.py
from django.conf import settings
from django.template.loader import render_to_string
from .providers.base import EmailMessage
# from .providers.smtp_provider import SMTPProvider
# from .providers.resend_provider import ResendProvider
# from .exceptions import EmailSendError
# from .models import EmailLog


# _PROVIDERS = {'resend': ResendProvider(), 'smtp': SMTPProvider()}

def send_email(*, to, subject, template_name, context, from_email=None, attachments=None):
    pass
#     to = to if isinstance(to, list) else [to]
#     message = EmailMessage(
#         to=to,
#         subject=subject,
#         html_body=render_to_string(template_name, context),
#         text_body=render_to_string(template_name.replace('.html', '.txt'), context),
#         from_email=from_email or settings.DEFAULT_FROM_EMAIL,
#         attachments=attachments,
#     )

#     for provider_name in settings.EMAIL_PROVIDER_PRIORITY:  # e.g. ['resend', 'smtp']
#         try:
#             _PROVIDERS[provider_name].send(message)
#             EmailLog.objects.create(to=to, subject=subject, provider=provider_name, status='sent')
#             return
#         except EmailSendError:
#             continue

#     EmailLog.objects.create(to=to, subject=subject, provider='none', status='failed')
#     raise EmailSendError('All providers failed')
