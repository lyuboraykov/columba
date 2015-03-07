#!/usr/bin/env python3

import pytest

from providers.sendgrid import SendGridProvider
from send_error import SendError
import init_test_objects

def test_sendgrid_send_positive():
    """Straightforward sendgrid send test. Will fail if an error is raised by the provider."""
    sendgrid_provider = SendGridProvider(init_test_objects.SENDGRID_TEST_AUTHENTICATION,
        init_test_objects.SENDGRID_TEST_USERNAME)
    test_message = init_test_objects.init_message()
    sendgrid_provider.send(test_message)

def test_sendgrid_send_wrong_authentication():
    """The provider should raise an SendError if it gets wrong authentication"""
    sendgrid_provider = SendGridProvider(init_test_objects.SENDGRID_TEST_AUTHENTICATION + 's',
        init_test_objects.SENDGRID_TEST_USERNAME)
    test_message = init_test_objects.init_message()
    with pytest.raises(SendError) as send_error:
        sendgrid_provider.send(test_message)
    assert send_error

def test_sendgrid_send_missing_recipients():
    """The provider should raise a SendError if it has missing recipients field"""
    sendgrid_provider = SendGridProvider(init_test_objects.SENDGRID_TEST_AUTHENTICATION + 's',
        init_test_objects.SENDGRID_TEST_USERNAME)
    test_message = init_test_objects.init_message()
    test_message.recipients = ''
    with pytest.raises(SendError) as send_error:
        sendgrid_provider.send(test_message)
    assert send_error

def test_sendgrid_send_missing_sender():
    """The provider should raise a SendError if it has missing sender field"""
    sendgrid_provider = SendGridProvider(init_test_objects.SENDGRID_TEST_AUTHENTICATION + 's',
        init_test_objects.SENDGRID_TEST_USERNAME)
    test_message = init_test_objects.init_message()
    test_message.sender = ''
    with pytest.raises(SendError) as send_error:
        sendgrid_provider.send(test_message)
    assert send_error