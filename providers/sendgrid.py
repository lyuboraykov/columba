#!/usr/bin/env python3

from providers.provider import Provider
import send_error

class SendGridProvider(Provider):
    """Avbstracts Sendgrid's python library to send email."""
    
    def send(self, message):
        """Sends email via Sendgrid, raises SendError if it fails."""
        client = sendgrid.SendGridClient(self.username, self.authentication, raise_errors=True)
        message = sendgrid.Mail()
        message.add_to(message.recipients)
        message.add_cc(message.cc)
        message.add_bcc(message.bcc)
        message.set_subject(message.subject)
        message.set_html(message.body)
        for attachment in message.attachments:
            message.add_attachment_stream(attachment.name, attachment.content_stream)
        message.set_from(message.sender)
        try:
            client.send(message)
        except SendGridClientError as client_error:
            raise SendError("Error occured in Sendgrid's client") from client_error
        except SendGridServerError as server_error:
            raise SendError("Error occured in Sendgrid's server") from server_error