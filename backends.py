import logging

from django.core.mail.backends.smtp import EmailBackend

_logger = logging.getLogger(__name__)


class LoggingEmailBackend(EmailBackend):

    def send_messages(self, email_messages):
        _logger.debug("Send %s email messages" % len(email_messages))
        try:
            nbr_sent = super().send_messages(email_messages)
            _logger.debug("%s email messages sent" % nbr_sent)
            return nbr_sent
        except Exception as e:
            _logger.error("exception during sending emails. %s", e)
            raise e
