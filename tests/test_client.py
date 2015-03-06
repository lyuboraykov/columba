#!/usr/bin/env python3

import pytest

from client import Client
from providers.provider import Provider
from message import Message

class TestProvider(Provider):
    def send(self, message):
        print('Test Message')

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