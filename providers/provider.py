#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

class Provider(metaclass=ABCMeta):
    """Abstract class for defining a mail-sender provider."""
    
    def __init__(self, username, authentication):
        """
        Default constructor, accepts the credentials for the service.
        authentication is either the password or the API token of the user.
        """
        self.username = username
        self.authentication = authentication

    @abstractmethod
    def send(self, sender, recipients, subject, body, cc=[], bcc=[], attachments=[]):
        """Default method for sending emails."""
        pass