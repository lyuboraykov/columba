#!/usr/bin/env python3

import pytest

import init_test_objects
import columba

def test_simple_parse():
    """Tests a parse of a request with single values for all parameters"""
    request = init_test_objects.init_simple_request()
    message = columba.get_message_from_request(request)
    assert message.sender == 'sender@columba.com'
    assert message.recipients == ['recipient@columba.com']
    assert message.cc == ['cc@columba.com']
    assert message.bcc == ['bcc@columba.com']
    assert message.subject == 'test subject'
    assert message.body == 'test body'
    assert len(message.attachments) == 1
    attachment = message.attachments[0]
    assert attachment.name == 'test_file'
    assert hasattr(attachment.content, 'read')

def test_multiple_recipients_parse():
    """Tests parsing a request with multiple recipients, cc and bcc"""
    request = init_test_objects.init_simple_request()
    request.form['to'] = 'recipient1@columba.com recipient2@columba.com'
    request.form['cc'] = 'cc1@columba.com cc2@columba.com'
    request.form['bcc'] = 'bcc1@columba.com bcc2@columba.com'
    message = columba.get_message_from_request(request)
    assert message.recipients == ['recipient1@columba.com', 'recipient2@columba.com']
    assert message.cc == ['cc1@columba.com', 'cc2@columba.com']
    assert message.bcc == ['bcc1@columba.com', 'bcc2@columba.com']

def test_only_mandatory_fields_parse():
    """
    Tests parsing a request that has only its mandatory fields.
    They are: sender, recipients, subject, body.
    The others should get their default values.
    """
    form = {
        'from': 'sender@columba.com',
        'to': 'recipient@columba.com',
        'subject': 'test subject',
        'body': 'test body'
    }
    request = init_test_objects.TestRequest(form)
    message = columba.get_message_from_request(request)
    assert message.cc == []
    assert message.bcc == []
    assert message.attachments == []

def test_request_with_missing_mandatory_fields():
    """When a mandatory field is missing it shoud raise KeyError"""
    mandatory_fields = ['from', 'to', 'subject', 'body']
    for field in mandatory_fields:
        request = init_test_objects.init_simple_request()
        request.form.pop(field)
        with pytest.raises(KeyError) as key_error:
            message = columba.get_message_from_request(request)
        assert key_error