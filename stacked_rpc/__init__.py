#!/usr/bin/python
# -*- coding: utf-8 -*-
"""methods to put a stack of servers / proxies together to one instance"""

def getServer(*stack):
    return getStacked('Server', *stack)

def getProxy(*stack):
    proxy = getStacked('Proxy', reverseStack=True, *stack)
    proxy.__repr__ = lambda: '<instance object of stacked_rpc.Proxy>'
    return proxy

def getStacked(target_name, *stack, **kwargs):
    if len(stack) == 1 and type(stack[0]) == type([]):
            stack = stack[0]
    stack = list(stack)

    if kwargs.get('reverseStack', False):
        stack.reverse()

    last_defined_target = None
    for target_definition in stack:

        if str(type(target_definition)) == "<type 'module'>":
            target_definition = (target_definition, {})
        assert len(target_definition) == 2

        target_module = target_definition[0]
        assert str(type(target_module)) == "<type 'module'>"

        target_kwargs = target_definition[1]
        assert type(target_kwargs) == type({})

        if last_defined_target != None:
            target_kwargs['next' + target_name] = last_defined_target

        last_defined_target = getattr(target_module, target_name)(**target_kwargs)

    return last_defined_target
