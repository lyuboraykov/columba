#!/usr/bin/env python3

import os
import logging
import flask
from flask import Flask, request, send_from_directory

from providers.sendgrid import SendGridProvider
from providers.mailgun import MailGunProvider
from client import Client
from message import Message
from send_error import SendError
from attachment import Attachment

app = Flask(__name__)
# Maximum of 16MB for file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
client = Client()

@app.route("/send", methods=['POST'])
def send():
    """
    Sends email according to the provided form data.
    Returns HTTP 200 if the mail is sent regardless of the provider it used.
    Returns HTTP 500 if an error occured and logs the error.
    """
    try:
        message = get_message_from_request(request)
        logging.info('Sending message {}'.format(message))
    except KeyError:
        logging.error('Missing mandatory fields in form request.')
        return 'sender, recipients, subject and body fields are mandatory.', 500
    try:
        client.send(message)
        logging.info('Sent message {}'.format(message))
        return 'Message was sent successfully', 200
    except SendError as e:
        logging.error('Message could not be sent: {}'.format(e))
        return 'Something wrong happened, email could not be sent.', 500

@app.route("/")
def index():
    """Provides a simple form to use the API with UI"""
    return send_from_directory('views', 'index.html')

def get_message_from_request(request):
    """Parses the POST parameters provided to the send method."""
    sender = request.form['sender']
    recipients = request.form['recipients'].split()
    subject = request.form['subject']
    body = request.form['body']
    cc = request.form.get('cc', '').split()
    bcc = request.form.get('bcc', '').split()
    attachments = parse_attachments(request)
    return Message(sender, recipients, subject, body, cc, bcc, attachments)

def parse_attachments(request):
    """Parses the attached files in the request as Attachment array"""
    attachments = []
    for attachment in request.files.getlist('attachment'):
        attachments.append(Attachment(attachment.filename, attachment))
    return attachments

@app.before_first_request
def initialize_client():
    """Initializes the main client on flask.g and registers providers to it."""
    logging.info('Initializing Sendgrid provider')
    sendgrid_authentication, sendgrid_username = get_provider_credentials('sendgrid') 
    sendgrid_provider = SendGridProvider(sendgrid_authentication, sendgrid_username)

    logging.info('Initializing Mailgun provider')
    mailgun_authentication, mailgun_domain = get_provider_credentials('mailgun')
    mailgun_provider = MailGunProvider(mailgun_authentication, mailgun_domain)

    logging.info('Registering providers')
    client.register_provider(sendgrid_provider, 10)
    client.register_provider(mailgun_provider, 20)

def get_provider_credentials(provider):
    """
    Provider credentials should be injected in the deployed instance as enviroment
    variables. It gets them as PROVIDER_USERNAME and PROVIDER_AUTHENTICATION
    PROVIDER_USERNAME is optional in case the provider uses API key.
    For example, for Sendgrid it would be SENDGRID_USERNAME and SENDGRID_AUTHENTICATION.
    """
    logging.info('Getting provider credentials for {}'.format(provider))
    uppercase_provider = provider.upper()
    username_variable = '{}_USERNAME'.format(uppercase_provider)
    authentication_variable = '{}_AUTHENTICATION'.format(uppercase_provider)
    username = os.environ.get(username_variable, '')
    authentication = os.environ[authentication_variable]
    return authentication, username

if __name__ == "__main__":
    app.run()