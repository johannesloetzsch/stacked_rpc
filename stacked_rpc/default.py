#!/usr/bin/python
# -*- coding: utf-8 -*-

from layer import prototype, send_dummy, marshall_xml, send_xmlrpclib, auth_simple
import stacked_rpc

def getDefaultServer(payload, psk=None, port=None):
    useDummy = port == None

    stack = []

    """dispatching"""
    stack.append((prototype, {'payload': payload}))

    """authentication"""
    if not useDummy:
        assert psk != None
        stack.append((auth_simple, {'psk': psk}))

    """marshalling"""
    if useDummy:
        stack.append((marshall_xml, {}))

    """sending server"""
    if useDummy:
        stack.append((send_dummy, {}))
    else:
        stack.append((send_xmlrpclib, {'port': port}))

    return stacked_rpc.getServer(stack)

def getDefaultProxy(psk=None, server=None, port=None):
    useDummy = port == None

    stack = []

    """authentication"""
    if not useDummy:
        assert psk != None
        stack.append((auth_simple, {'psk': psk}))
    
    """marshalling"""
    if useDummy:
        stack.append((marshall_xml, {}))
    
    """sending proxy"""
    if useDummy:
        assert server != None, 'Either server or port needed'
        stack.append((send_dummy, {'server': server}))
    else:
        stack.append((send_xmlrpclib, {'port': port}))

    return stacked_rpc.getProxy(stack)