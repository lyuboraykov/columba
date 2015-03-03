#!/usr/bin/env python3

import heapq

class Client(object):
    """Email proxy client. Abstracts registered providers."""

    providers = []
    
    def send(self, sender, recipients, cc, bcc, subject, body, attachments):
        """
        Sends an email.
        Uses the registered providers and failsover basen on their priority.
        """
        providers_copy = list(providers)
        error_message = ''
        is_mail_sent = False
        while len(providers_copy) > 0:
            current_provider = heappop(providers_copy)
            try:
                current_provider.send(sender, recipients, cc, bcc, subject, body, attachments)
                is_mail_sent = True
                break
            except SendError as e:
                error_message += 'Provider failed with: {}; \n'.format(e.value)
        if not is_mail_sent:
            raise SendError(error_message)
        return
    
    def register_provider(self, provider, priority):
        """Adds the providers to a heap based on their priority."""
        heappush(providers, (priority, provider))