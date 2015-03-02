class SendError(Exception):
    """Error raised when sending email."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)