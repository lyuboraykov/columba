#!/usr/bin/env python3

import requests

from providers.provider import Provider
from send_error import SendError

class MailGunProvider(Provider):
    """Avbstracts Sendgrid's python library to send email."""
    def send(self, message):
        """Sends email via Mailgun's API. Uses requests to make a POST request."""
        # Mailgun gives its users the ability to use custom domains and
        # uses them as identifiers
        mailgun_domain = self.username
        post_url = "https://api.mailgun.net/v2/{}/messages".format(mailgun_domain)
        api_key = self.authentication
        files_tuples = [('attachment', (a.name, a.content)) for a in message.attachments]
        response = requests.post(
                            post_url,
                            auth=("api", api_key),
                            data={
                                "from": message.sender,
                                "to": message.recipients,
                                "cc": message.cc,
                                "bcc": message.bcc,
                                "subject": message.subject,
                                "text": message.body
                            },
                            files=files_tuples
                        )
        if response.status_code != 200:
            error_message = "Mailgun request returned {}. Error is: {}".format(response.status_code, 
                response.text)
            raise SendError(error_message)
