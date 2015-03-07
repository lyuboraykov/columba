#!/usr/bin/env python3

import tempfile

from attachment import Attachment
from message import Message

class TestRequest(object):
    """Mock request class for flask's request object"""

    def __init__(self, form, files={}):
        """
        form -- dictionary with POST form parameters
        files - dictionary with posted files 
        """
        self.form = form
        self.files = files

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
    temporary_file = tempfile.TemporaryFile()
    files = {
        'test_file': temporary_file
    }
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