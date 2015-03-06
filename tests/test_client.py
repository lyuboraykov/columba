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
