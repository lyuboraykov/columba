#!/usr/bin/env python3

class Attachment(object):
    """Represents email attachment"""
    
    def __init__(self, name, content):
        self.name = name
        self.content = content