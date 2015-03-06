#!/usr/bin/env python3

import heapq
from send_error import SendError

class Client(object):
    """Email proxy client. Abstracts registered providers."""

    def __init__(self):
        self.providers = []
    
    def send(self, message):
        """
        Sends an email.
        Uses the registered providers and failsover basen on their priority.
        """
        providers_copy = list(self.providers)
        error_message = ''
        is_mail_sent = False
        while len(providers_copy) > 0:
            current_provider = heapq.heappop(providers_copy)[1] # it's a tuple with priority
            try:
                current_provider.send(message)
                is_mail_sent = True
                break
            except SendError as e:
                error_message += 'Provider failed with: {}; \n'.format(e.value)
        if not is_mail_sent:
            raise SendError(error_message)
        return
    
    def register_provider(self, provider, priority):
        """Adds the providers to a heap based on their priority."""
        heapq.heappush(self.providers, (priority, provider))