#!/usr/bin/env python3

from providers.provider import Provider
from sendgrid import SendGridClient, Mail, SendGridClientError, SendGridServerError
from send_error import SendError

class SendGridProvider(Provider):
    """Avbstracts Sendgrid's python library to send email."""
    
    def send(self, message):
        """Sends email via Sendgrid, raises SendError if it fails."""
        client = SendGridClient(self.username, self.authentication, raise_errors=True)
        sendgrid_message = Mail()
        sendgrid_message.add_to(message.recipients)
        sendgrid_message.add_cc(message.cc)
        sendgrid_message.add_bcc(message.bcc)
        sendgrid_message.set_subject(message.subject)
        sendgrid_message.set_html(message.body)
        for attachment in message.attachments:
            sendgrid_message.add_attachment_stream(attachment.name, attachment.content_stream)
        sendgrid_message.set_from(message.sender)
        try:
            client.send(sendgrid_message)
        except SendGridClientError as client_error:
            raise SendError("Error occured in Sendgrid's client") from client_error
        except SendGridServerError as server_error:
            raise SendError("Error occured in Sendgrid's server") from server_error