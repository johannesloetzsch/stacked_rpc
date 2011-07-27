#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
### testdata and class with functions for testing ###
>>> testdata = [1, 'zwei', {'und': 3}]
>>> expected = [testdata, 1337]
>>> assert Testclass().extended_pong(testdata) == expected
>>> testport = 8888

### test sending with dummy ###
>>> serverDummy = send_dummy.Server(payload=Testclass)
>>> proxyDummy = send_dummy.Proxy(server=serverDummy)
>>> proxyDummy
<instance object of stacked_rpc.layer.send_dummy.Proxy>
>>> proxyDummy.system.listMethods()
['extended_pong', 'system.listMethods']
>>> assert proxyDummy.extended_pong(testdata) == expected

### test marshalling with dummy ###
>>> serverMarshall = marshall_xml.Server(payload=Testclass)
>>> serverMarshallDummy = send_dummy.Server(nextServer=serverMarshall)
>>> proxyDummy_to_MarshallDummy = send_dummy.Proxy(server=serverMarshallDummy)
>>> proxyMarshallDummy = marshall_xml.Proxy(nextProxy=proxyDummy_to_MarshallDummy)
>>> proxyMarshallDummy
<instance object of stacked_rpc.layer.marshall_xml.Proxy>
>>> proxyMarshallDummy.system.listMethods()
['extended_pong', 'system.listMethods']
>>> assert proxyMarshallDummy.extended_pong(testdata) == expected

### test the same using stacked_rpc ###
>>> server = stacked_rpc.getServer([ (marshall_xml, {'payload': Testclass}), (send_dummy, {}) ])
>>> proxy = stacked_rpc.getProxy([ (marshall_xml, {}), (send_dummy, {'server': server}) ])
>>> proxy
<instance object of stacked_rpc.Proxy>
>>> proxy.system.listMethods()
['extended_pong', 'system.listMethods']
>>> assert proxy.extended_pong(testdata) == expected

### same with reduced arguments ###
>>> server = stacked_rpc.getServer((marshall_xml, {'payload': Testclass}), send_dummy)
>>> proxy = stacked_rpc.getProxy(marshall_xml, (send_dummy, {'server': server}))
>>> assert proxy.extended_pong(testdata) == expected

### test module as payload ###
>>> server = stacked_rpc.getServer((marshall_xml, {'payload': math}), send_dummy)
>>> proxy = stacked_rpc.getProxy(marshall_xml, (send_dummy, {'server': server}))
>>> assert 'floor' in proxy.system.listMethods()
>>> proxy.floor( 1337 * proxy.pi() / 100 )
42.0

### test a real (non-dummy) server ###
>>> server = send_xmlrpclib.Server(port=testport, payload=Testclass)
>>> proxy = send_xmlrpclib.Proxy(port=testport)
>>> server.stop()

### use server with auth ###
>>> psk = str(random.randint(0, 2**256))
>>> server = stacked_rpc.getServer((auth_simple, {'payload': Testclass, 'psk': psk}), send_dummy)
>>> proxy = stacked_rpc.getProxy((auth_simple, {'psk': psk}), (send_dummy, {'server': server}))
>>> assert proxy.extended_pong(testdata) == expected

>>> proxy_wrongPsk = stacked_rpc.getProxy((auth_simple, {'psk': 'wrong'}), (send_dummy, {'server': server}))
>>> proxy_wrongPsk.extended_pong(testdata).get('exception_type')
'AuthTokenError'

>>> server_newSession = stacked_rpc.getServer((auth_simple, {'payload': Testclass, 'psk': psk}), send_dummy)
>>> proxy.nextProxy.server = server_newSession
>>> proxy.extended_pong(testdata).get('exception_type')
'ReconnectionWarning'
>>> assert proxy.extended_pong(testdata) == expected

### use minimal default-server/proxy ###
>>> server = stacked_rpc.default.getDefaultServer(payload=Testclass)
>>> proxy = stacked_rpc.default.getDefaultProxy(server=server)
>>> assert proxy.extended_pong(testdata) == expected

### use recommended default-server/proxy ###
>>> server = stacked_rpc.default.getDefaultServer(payload=Testclass, psk=psk, port=testport)
>>> proxy = stacked_rpc.default.getDefaultProxy(psk=psk, port=testport)
>>> assert proxy.extended_pong(testdata) == expected
>>> server.stop()
"""

import doctest
from pprint import pprint

from stacked_rpc.layer import send_dummy, marshall_xml, send_xmlrpclib, auth_simple
import stacked_rpc
import stacked_rpc.default

import math
import random

class Testclass():
    def extended_pong(self, arg):
        return [arg, 1337]

if __name__ == '__main__':
    print doctest.testmod()
