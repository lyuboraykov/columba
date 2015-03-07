#!/usr/bin/env python3

import pytest

import columba

def test_send_positive():
    """Tests calling the /send method with a sample message."""
    test_client = columba.app.test_client()
    response = test_client.post('/send', data={
        'sender': 'sender@columba.com',
        'recipients': 'recipient@columba.com',
        'subject': 'test subject',
        'body': 'test body'
    })
    assert response.status_code == 200

def test_send_missing_fields():
    """Tests calling the /send method with missing mandatory recipients field"""
    test_client = columba.app.test_client()
    response = test_client.post('/send', data={
        'sender': 'sender@columba.com',
        'subject': 'test subject',
        'body': 'test body'
    })
    assert response.status_code == 500