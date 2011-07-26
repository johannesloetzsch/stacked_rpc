#!/usr/bin/python
# -*- coding: utf-8 -*-
"""every implementation of a layer/send-module should inherit from this Server&Proxy"""

import stacked_rpc.system

import threading
import time
import select

class Server():
    """Prototype of server (but already working when dispatch is called from outside).
       When you implement your own server, you should only need to overwrite the dispatch-method
       … and of course listen for requests and trigger dispatch for each of them"""

    def __init__(self, nextServer=None, host=None, port=None, payload=None, startIn='background', allow_none=True):
        self.nextServer = nextServer

        if port != None:
            if host == None:
                host = 'localhost'
            self.port = port
            self.host = host
            self.uri = 'http://' + host + ':' + str(port)

        self.payload = instanceOf(payload)
        if payload != None:
            self.payload.system = stacked_rpc.system.System(server=self)

        self.startIn = startIn
        self.allow_none = allow_none

        if hasattr(self, 'start'):
            self.start()

    def dispatch(self, method, params):
        """overwrite this in your implementation"""
        return self.dispatch_next(method, params)

    def dispatch_next(self, method, params):
        """if your implementation of layer is not finally dispatching (but reencoding),
           you can use this within dispatch to call dispatch-method of next layer"""

        if self.nextServer == None:
            return self.dispatch_finally(method, params)

        return self.nextServer.dispatch(method, params)

    def dispatch_finally(self, method, params):
        """find called method in payload"""

        obj_at_payload = self.payload
        for subobj in method.split('.'):
            assert hasattr(obj_at_payload, subobj), 'Not in payload: ' + str(obj_at_payload) + '.' + subobj
            obj_at_payload = getattr(obj_at_payload, subobj)

        if hasattr(obj_at_payload, '__call__'):
            return obj_at_payload(*params)
        else:
            """get property as method with arity 0"""
            return obj_at_payload

    def startThread(self):
        """can be called by your implementation of start"""
        assert hasattr(self, 'server_thread_target')
        if self.startIn == 'foreground':
            self.startForeground()
        else:
            self.server_thread = threading.Thread(target=self.server_thread_target)
            self.server_thread.setDaemon(True)
            self.server_thread.start()

    def startForeground(self):
        try:
            self.server_thread_target()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print '\n'
        except select.error:
            print '\n'
        finally:
            self.stop()


class Proxy():
    """This prototype of proxy binds a proxy-object to the send-method (via GetAttrRecursive)
       If you implement your own proxy, you should only need to overwrite the send-method"""

    def __init__(self, nextProxy=None, host=None, port=None, payload=None, allow_none=True):
        self.nextProxy = nextProxy

        if port != None:
            if host == None:
                host = 'localhost'
            self.port = port
            self.host = host
            self.uri = 'http://' + host + ':' + str(port)

        self.payload = payload

        self.allow_none = allow_none

    def send(self, method, params):
        """implement it in instance of this prototype"""
        raise NotImplementedError, str(self.__class__) + '.send'

    def send_next(self, method, params):
        """if your implementation of layer is not finally sending (but reencoding),
           you can use this within send to call send-method of next layer"""

        assert type(params) == type(()), 'params needs to be tuple, but is ' + str(type(params))
        nextProxy = self.nextProxy
        assert self.nextProxy != None, 'send_next not possible for last proxy in stack'
        return self.nextProxy.send(method, params)

    def __getattr__(self, name):
        return Proxy.GetAttrRecursive(self, name)

    def __repr__(self):
        return '<instance object of ' + str(self.__class__) + '>'

    def __ne__(self, obj):
        if obj.__class__ != self.__class__:
            return True
        else:
            """we don't know"""

    class GetAttrRecursive:
        """„magic“ to bind an RPC-method (call will result in send-function of proxy)"""

        def __init__(self, proxy, name):
            self.__proxy = proxy
            self.__name = name

        def __getattr__(self, name):
            """recurse into subobject"""
            return Proxy.GetAttrRecursive(self.__proxy, "%s.%s" % (self.__name, name))

        def __call__(self, *args):
            """Ignore"""
            for suffix in ['trait_names', 'getdoc', '__str__', '__len__', '__radd__', '__coerce__']:
                if self.__name.split('.')[-1] == suffix:
                    return None
            """For tab-completion"""
            for suffix in ['_getAttributeNames']:
                if self.__name.split('.')[-1] == suffix:
                    path = self.__name[:-len(suffix)]
                    return [i[len(path):] for i in self.__proxy.send('system.listMethods', ()) if i.startswith(path)]
            """Method on Server"""
            return self.__proxy.send(self.__name, args)


def instanceOf(obj):
    if str(type(obj)) == "<type 'classobj'>":
        return obj()
    return obj
