#!/usr/bin/python
# -*- coding: utf-8 -*-

from layer import prototype, send_dummy, marshall_xml, send_xmlrpclib, auth_simple, show_ipy
import stacked_rpc

import socket

def getDefaultServer(payload, psk=None, port=None, startIn='background'):
    useDummy = port == None

    stack = []

    """dispatching"""
    stack.append((prototype, {'payload': payload}))

    """authentication"""
    if not useDummy:
        stack.append((auth_simple, {'psk': psk}))

    """marshalling"""
    if useDummy:
        stack.append((marshall_xml, {}))

    """sending server"""
    if useDummy:
        stack.append((send_dummy, {}))
    else:
        stack.append((send_xmlrpclib, {'port': port, 'startIn': startIn}))

    """show ipy"""
    if startIn == 'ipy':
        stack.append((show_ipy, {}))

    return stacked_rpc.getServer(stack)

def getDefaultProxy(psk=None, server=None, port=None, useDummy=None):
    if useDummy == None:
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

def getDefaultProxy_fallbackDummy(psk, payload, port):

    try:
        return getDefaultProxy(useDummy=False, psk=psk, port=port)
    except socket.error:
        if payload != None:
            server_dummy = getDefaultServer(payload=payload)
            return getDefaultProxy(useDummy=True, server=server_dummy)
