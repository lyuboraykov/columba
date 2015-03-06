#!/usr/bin/env python3

import pytest

from client import Client
from providers.provider import Provider
from message import Message
from send_error import SendError

class TestProvider(Provider):
    def send(self, message):
        """Dummy test method for testing purposes"""
        print('Test Message')

class FailingProvider(Provider):
    def send(self, message):
        """Dummy send which raises an error."""
        raise SendError("Test error")

def test_register_provider():
    client = Client()
    test_provider = TestProvider('username', 'password')
    client.register_provider(test_provider, 10)
    assert len(client.providers) == 1

def test_sending_with_single_provider(capsys):
    client = Client()
    test_provider = TestProvider('username', 'password')
    client.register_provider(test_provider, 10)
    message = Message('sender', ['recipient'], 'subject', 'body')
    client.send(message)
    out, err = capsys.readouterr()
    assert out == 'Test Message\n'

def test_registering_muiltiple_providers():
    client = Client()
    test_provider1 = TestProvider('username', 'password')
    test_provider2 = TestProvider('username', 'password')
    client.register_provider(test_provider1, 10)
    client.register_provider(test_provider2, 20)
    assert len(client.providers) == 2

def test_provider_failover(capsys):
    client = Client()
    print_provider = TestProvider('username', 'password')
    failing_provider = FailingProvider('username', 'password')
    client.register_provider(failing_provider, 10)
    client.register_provider(print_provider, 20)
    message = Message('sender', ['recipient'], 'subject', 'body')
    client.send(message)
    out, err = capsys.readouterr()
    assert out == 'Test Message\n'

def test_multiple_failing_providers():
    client = Client()
    failing_provider1 = FailingProvider('username', 'password')
    failing_provider2 = FailingProvider('username', 'password')
    client.register_provider(failing_provider1, 10)
    client.register_provider(failing_provider2, 20)
    message = Message('sender', ['recipient'], 'subject', 'body')
    with pytest.raises(SendError) as send_error:
        client.send(message)
    assert send_error