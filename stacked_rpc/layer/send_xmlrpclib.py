#!/usr/bin/python
# -*- coding: utf-8 -*-
"""send over xmlrpc"""

import prototype

import xmlrpclib
import SimpleXMLRPCServer

import threading
import time

class Server(prototype.Server):

    def start(self):
        assert not hasattr(self, 'server_thread') or not self.server_thread.is_alive(), 'already running'

        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer(addr=(self.host, self.port), allow_none=self.allow_none)
        self.server.register_instance(self.payload, allow_dotted_names=True)
        self.server._dispatch = self.dispatch

        self.server_thread_target = self.server.serve_forever
        self.startThread()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

class Proxy(prototype.Proxy):

    def __init__(self, **kwargs):
        prototype.Proxy.__init__(self, **kwargs)
        self.proxy = xmlrpclib.ServerProxy(self.uri, allow_none=self.allow_none)

    def send(self, method, params):
        return self.proxy._ServerProxy__request(method, params)
