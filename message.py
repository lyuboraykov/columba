#!/usr/bin/env python3

class Message(object):
    """Contains fields for a typical email message"""

    def __init__(self, sender, recipients, subject, body, cc=[], bcc=[], attachments=[]):
        """Constructor, cc, bcc and attachments are optional"""
        self.sender = sender
        self.recipients = recipients
        self.subject = subject
        self.body = body
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments