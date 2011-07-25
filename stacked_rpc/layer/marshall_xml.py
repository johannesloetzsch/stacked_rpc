#!/usr/bin/python
# -*- coding: utf-8 -*-
"""params is encoded to 1-element-tuple of xml-string encoding original param-tuple
   result is encoded to xml-string

   In opposite to xmlrpclib.Server, the method-name will not be included to encoded string
"""

import prototype

import xmlrpclib


class Server(prototype.Server):

    def __init__(self, allow_none=True, **kwargs):
        self.allow_none = allow_none
        prototype.Server.__init__(self, **kwargs)

    def dispatch(self, method, params):
        assert type(params[0]) == type('')
        params = tuple( decode(params[0]) )
        result = self.dispatch_next(method, params)
        return encode(result, allow_none=self.allow_none)


class Proxy(prototype.Proxy):

    def __init__(self, allow_none=True, **kwargs):
        self.allow_none = allow_none
        prototype.Proxy.__init__(self, **kwargs)

    def send(self, method, params):
        params = tuple([ encode(params, allow_none=self.allow_none) ])
        result = self.send_next(method, params)
        return decode(result)
    

def encode(value, allow_none):
    return xmlrpclib.dumps(tuple([ value ]), allow_none=allow_none)

def decode(value):
    return xmlrpclib.loads( value )[0][0]
