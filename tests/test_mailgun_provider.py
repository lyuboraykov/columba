#!/usr/bin/env python3

import pytest

from providers.mailgun import MailGunProvider
from send_error import SendError
import init_test_objects

def test_mailgun_send_positive():
    """Straightforward mailgun send test. Will fail if an error is raised by the provider."""
    mailgun_provider = MailGunProvider(init_test_objects.MAILGUN_TEST_AUTHENTICATION,
        init_test_objects.MAILGUN_TEST_DOMAIN)
    test_message = init_test_objects.init_message()
    mailgun_provider.send(test_message)

def test_sendgrid_send_wrong_authentication():
    """The provider should raise an SendError if it gets wrong authentication"""
    mailgun_provider = MailGunProvider(init_test_objects.MAILGUN_TEST_AUTHENTICATION + 's',
        init_test_objects.MAILGUN_TEST_DOMAIN)
    test_message = init_test_objects.init_message()
    with pytest.raises(SendError) as send_error:
        mailgun_provider.send(test_message)
    assert send_error

def test_sendgrid_send_missing_recipients():
    """The provider should raise a SendError if it has missing recipients field"""
    mailgun_provider = MailGunProvider(init_test_objects.MAILGUN_TEST_AUTHENTICATION + 's',
        init_test_objects.MAILGUN_TEST_DOMAIN)
    test_message = init_test_objects.init_message()
    test_message.recipients = ''
    with pytest.raises(SendError) as send_error:
        mailgun_provider.send(test_message)
    assert send_error

def test_sendgrid_send_missing_recipients():
    """The provider should raise a SendError if it has missing sender field"""
    mailgun_provider = MailGunProvider(init_test_objects.MAILGUN_TEST_AUTHENTICATION + 's',
        init_test_objects.MAILGUN_TEST_DOMAIN)
    test_message = init_test_objects.init_message()
    test_message.sender = ''
    with pytest.raises(SendError) as send_error:
        mailgun_provider.send(test_message)
    assert send_error