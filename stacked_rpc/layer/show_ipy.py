#!/usr/bin/python
# -*- coding: utf-8 -*-

import prototype
from prototype import Proxy

import IPython, sys


class Server(prototype.Server):

    def __init__(self, startIn=None, **kwargs):

        prototype.Server.__init__(self, **kwargs)

        print 'Exit ipy with ctrl+d to stop server'
        sys.argv = []
        IPython.Shell.IPShellEmbed(user_ns=locals())()
