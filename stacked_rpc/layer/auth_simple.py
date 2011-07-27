#!/usr/bin/python
# -*- coding: utf-8 -*-
"""handle a rpc-request using challenge-response-like procedure
    First parameter will be used to send an authentication-token:
    (counter, hash(counter + psk + session_nonce))

    check:
    => counter musst be bigger than last used one
    => hash musst be correct => client needs to know psk

    * session_nonce assures that challenge can not be reused in later session
    ** client can query it from server

    Only should protect against unauthorized clients…
    …no synchronization of counters from different clients
    => assuming no competing clients
"""

import prototype

import random, time, hashlib

class Server(prototype.Server):

    def __init__(self, psk, **kwargs):
        if psk == None:
            psk = str(random.randint(0, 2**256))
            print 'Used PSK: ' + psk
        assert type(psk) == type('')
        self.psk = psk

        prototype.Server.__init__(self, **kwargs)
        self.session_nonce = str(random.randint(0, 2**256))
        self.token_counter_exhausted = 0

    def dispatch(self, method, params):

        if method == '__get_session_nonce__':
            return self.session_nonce

        else:
            (next_params, auth_token) = params
            auth_token = tuple(auth_token)
            (token_counter, hashed_salted_secret) = auth_token
            if not self.token_counter_exhausted < token_counter:
                return {'auth-error': True,
                        'error': True,
                        'exception_type': 'ExhaustedTokenError',
                        'exception_msg': 'token_counter needs to be bigger',
                        'stack': ''}

            auth_token_expected = calc_auth_token(token_counter, self.psk, self.session_nonce)
            if auth_token != auth_token_expected:
                return {'auth-error': True,
                        'error': True,
                        'exception_type': 'AuthTokenError',
                        'exception_msg': 'hash not matching => wrong PSK or new Session',
                        'stack': ''}

            self.token_counter_exhausted = token_counter
            return self.dispatch_next(method, next_params)

class Proxy(prototype.Proxy):

    def __init__(self, psk, silent_reconnect=False, **kwargs):
        self.psk = psk
        self.silent_reconnect = silent_reconnect
        prototype.Proxy.__init__(self, **kwargs)
        self.get_session_nonce()

    def get_session_nonce(self):
        self.session_nonce = self.send_next('__get_session_nonce__', tuple([]))

    def send(self, method, params, try_reconnect=True):
        token_counter = time.time()
        auth_token = calc_auth_token(token_counter, self.psk, self.session_nonce)
        result = self.send_next(method, (params, auth_token))

        if type(result) == type({}) and result.get('auth-error', False) and try_reconnect:
            old_session_nonce = self.session_nonce
            self.get_session_nonce()
            if old_session_nonce != self.session_nonce:
                result.update({'exception_type': 'ReconnectionWarning',
                               'exception_msg': 'Server has new Session - maybe state of server is lost'})
            if self.silent_reconnect:
                return self.send(method, params, try_reconnect=False)

        return result

def calc_auth_token(token_counter, psk, session_nonce):
    salted_secret = str(token_counter) + psk + session_nonce
    hashed_salted_secret = hashlib.sha256(salted_secret).hexdigest()
    return (token_counter, hashed_salted_secret)
