#!/usr/bin/env python3

import os
from flask import Flask, request
from providers.sendgrid import SendGridProvider
from client import Client
from message import Message
from send_error import SendError
from attachment import Attachment

app = Flask(__name__)
# Maximum of 16MB for file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
columba_client = Client()

@app.route("/send", methods=['POST'])
def send():
    """
    Sends email according to the provided form data.
    Returns HTTP 200 if the mail is sent regardless of the provider it used.
    Returns HTTP 500 if an error occured and logs the error.
    """
    try:
        message = get_message_from_form_data(request)
    except KeyError:
        return 'sender, recipients, subject and body fields are mandatory.', 500
    try:
        columba_client.send(message)
        return 'Message was sent successfully', 200
    except SendError as e:
        print(e)
        return 'Something wrong happened, email could not be sent.', 500
    return "Mail sent! {}".format(message)

def get_message_from_form_data(request):
    """Parses the POST parameters provided to the send method."""
    sender = request.form['sender']
    recipients = request.form['recipients'].split(',')
    subject = request.form['subject']
    body = request.form['body']
    cc = request.form.get('cc', default=[])
    bcc = request.form.get('bcc', default=[])
    attachments = parse_attachments(request)
    return Message(sender, recipients, subject, body, cc, bcc, attachments)

def parse_attachments(request):
    """Parses the attached files in the request as Attachment array"""
    attachments = []
    for name, file_content in request.files.items():
        attachments.append(Attachment(name, file_content.read()))
    return attachments

@app.before_first_request
def register_providers():
    """Registers available providers to the main columba_client"""
    sendgrid_username, sendgrid_authentication = get_provider_credentials('sendgrid') 
    sendgrid_provider = SendGridProvider(sendgrid_username, sendgrid_authentication)
    columba_client.register_provider(sendgrid_provider, 10)

def get_provider_credentials(provider):
    """
    Provider credentials should be injected in the deployed instance as enviroment
    variables. It gets them as PROVIDER_USERNAME and PROVIDER_AUTHENTICATION
    For example, for Sendgrid it would be SENDGRID_USERNAME and SENDGRID_AUTHENTICATION.
    """
    uppercase_provider = provider.upper()
    username_variable = '{}_USERNAME'.format(uppercase_provider)
    authentication_variable = '{}_AUTHENTICATION'.format(uppercase_provider)
    username = os.environ[username_variable]
    authentication = os.environ[authentication_variable]
    return username, authentication

if __name__ == "__main__":
    app.debug = True
    app.run()