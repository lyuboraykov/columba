#!/usr/bin/env python3

import os
import pytest

import app

def test_get_provider_credentials():
    os.environ['TESTPROVIDER_USERNAME'] = 'testprovider_username'
    os.environ['TESTPROVIDER_AUTHENTICATION'] = 'testprovider_authentication'
    authentication, username = app.get_provider_credentials('testprovider')
    assert authentication == 'testprovider_authentication'
    assert username == 'testprovider_username'