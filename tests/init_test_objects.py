#!/usr/bin/env python3

import tempfile
import os

from attachment import Attachment
from message import Message

MAILGUN_TEST_DOMAIN = 'sandbox5faa34abe01446d5be16abc8077cb531.mailgun.org'
MAILGUN_TEST_AUTHENTICATION = 'key-b5b8a218881f2d7c34b7fb14fe5deb0f'
SENDGRID_TEST_USERNAME = 'lyuboraykov'
SENDGRID_TEST_AUTHENTICATION = 'columbap@22'

class TestFile(object):
    """Mock file that has filename and read() attributes"""
    filename="test_file"
    def read(self):
        pass

class TestRequest(object):
    """Mock request class for flask's request object"""

    def __init__(self, form, files=[]):
        """
        form -- dictionary with POST form parameters
        files - dictionary with posted files 
        """
        self.form = form
        self.files = TestFilesList(files)

class TestFilesList(object):
    """Mock class that provides the getlist method to return file objects"""

    def __init__(self, files):
        self.files = files

    def getlist(self, key):
        """It is used to get the attachments of the request"""
        if key == 'attachment':
            return self.files

def init_simple_request():
    """Create a request with single values for all fields"""
    form = {
        'sender': 'sender@columba.com',
        'recipients': 'recipient@columba.com',
        'cc': 'cc@columba.com',
        'bcc': 'bcc@columba.com',
        'subject': 'test subject',
        'body': 'test body'
    }
    test_file = TestFile()
    files = [test_file]
    request = TestRequest(form, files)
    return request

def init_message():
    """Returns a sample message for the provider to send"""
    sender = 'sender@columba.com'
    recipients = ['recipients@columba.com']
    subject = 'Test subject'
    body = 'Test body'
    cc = ['cc@columba.com']
    bcc = ['bcc@columba.com']
    temporary_file = tempfile.TemporaryFile()
    attachments = [Attachment('test_attachment', temporary_file)]
    message = Message(sender, recipients, subject, body, cc, bcc, attachments)
    return message

def init_env_variables():
    """Initializes environment variables for the supported providers."""
    os.environ['SENDGRID_USERNAME'] = SENDGRID_TEST_USERNAME
    os.environ['SENDGRID_AUTHENTICATION'] = SENDGRID_TEST_AUTHENTICATION
    os.environ['MAILGUN_USERNAME'] = MAILGUN_TEST_DOMAIN
    os.environ['MAILGUN_AUTHENTICATION'] = MAILGUN_TEST_AUTHENTICATION
