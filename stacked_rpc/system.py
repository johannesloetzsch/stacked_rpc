#!/usr/bin/python
# -*- coding: utf-8 -*-

class System():
    """system-methods available via rpc
    it will be imported as subclass of payload"""

    def __init__(self, server):
        self.server = server

    def listMethods(self):
        supported_types = ["<type 'instancemethod'>", "<type 'builtin_function_or_method'>"]
        return [method for method in dir(self.server.payload)
                if not method.startswith('_')
                and str(type(getattr(self.server.payload, method))) in supported_types] + \
               ['system.' + sysmethod for sysmethod in dir(self)
                if not sysmethod.startswith('_')
                and str(type(getattr(self, sysmethod))) in supported_types]
