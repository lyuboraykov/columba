#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod

class Provider(metaclass=ABCMeta):
    """Abstract class for defining a mail-sender provider."""
    
    def __init__(self, authentication, username=''):
        """
        Default constructor, accepts the credentials for the service.
        The username is optional in case the provider uses only API key.
        authentication is either the password or the API token of the user.
        """
        self.username = username
        self.authentication = authentication

    @abstractmethod
    def send(self, message):
        """Default method for sending emails."""
        pass