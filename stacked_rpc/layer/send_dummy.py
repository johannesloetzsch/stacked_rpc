#!/usr/bin/python
# -*- coding: utf-8 -*-
"""shortcut to payload — (without listening server)"""

import prototype
from prototype import Server

class Proxy(prototype.Proxy):

    def __init__(self, server, **kwargs):
        self.server = server
        prototype.Proxy.__init__(self, **kwargs)

    def send(self, method, params):
        return self.server.dispatch(method, params)
