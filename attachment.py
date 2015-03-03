#!/usr/bin/env python3

class Attachment(object):
    """Represents email attachment"""
    
    def __init__(self, name, content_stream):
        self.name = name
        self.content_stream = content_stream