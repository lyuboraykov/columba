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
    def send(self, sender, recipient, cc, bcc, subject, body, attachments):
        """Default method for sending emails."""
        pass