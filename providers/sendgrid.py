#!/usr/bin/env python3

import provider
import sendgrid
import send_error

class SendGridProvider(Provider):
    """Avbstracts Sendgrid's python library to send email."""
    
    def send(self, sender, recipients, subject, body, cc=[], bcc=[], attachments=[]):
        """Sends email via Sendgrid, raises SendError if it fails."""
        client = sendgrid.SendGridClient(self.username, self.authentication, raise_errors=True)
        message = sendgrid.Mail()
        message.add_to(recipients)
        message.add_cc(cc)
        message.add_bcc(bcc)
        message.set_subject(subject)
        message.set_html(body)
        for attachment in attachments:
            message.add_attachment_stream(attachment.name, attachment.content_stream)
        message.set_from(sender)
        try:
            client.send(message)
        except SendGridClientError as client_error:
            raise SendError("Error occured in Sendgrid's client") from client_error
        except SendGridServerError as server_error:
            raise SendError("Error occured in Sendgrid's server") from server_error