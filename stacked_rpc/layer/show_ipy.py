#!/usr/bin/python
# -*- coding: utf-8 -*-
"""attaches server to an ipython-console
this needs to be last server in stack"""

import prototype
from prototype import Proxy

import IPython, sys

class Server(prototype.Server):

    def __init__(self, startIn=None, **kwargs):

        prototype.Server.__init__(self, **kwargs)

        print 'Exit ipy with ctrl+d to stop server'
        sys.argv = []
        IPython.Shell.IPShellEmbed(user_ns=locals())()
