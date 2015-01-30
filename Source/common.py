# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 20:12:33 2014

@author: Misha
"""


class FunctionsWrapper(object):
    """A class that holds functions to do stuff with."""

    def __init__(self):
        self.history = {}

    def _updhst(self, cmd, args):
        """Update cmd history."""
        num = len(self.history)
        adding = {num: {'cmd': cmd, 'args': args}}
        self.history.update(adding)

    def call(self, func, *args, **kwargs):
        """Call specified func with args and/or kwargs."""
        self._updhst('call', {'func': func, 'args': args, 'kwargs': kwargs})
        r = func(*args, **kwargs)
        return r

    def getmodule(self, name, failed=None):
        """Given a module name in string format, such as 'os', return the specified
        module or return the optional `failed` argument (default=None)"""
        self._updhst('getmodule', {'name': name, 'failed': failed})
        try:
            returnObj = __import__(name)
            return returnObj
        except ImportError:
            return failed

    def getmodules(self, *names):
        """Plural form of getmodule."""
        self._updhst('getmodules', {'names': names})
        r = []
        for name in names:
            r.append(self.getmodule(name))
        return r

    def getcommon(self):
        """Import and global-ify a series of common modules: sys, os, math."""
        self._updhst('getcommon', {})
        global sys
        sys = self.getmodule('sys')
        global os
        os = self.getmodule('os')
        global math
        math = self.getmodule('math')

    def deepcopy(self, iterable):
        """Return a deep copy of an iterable."""
        self._updhst('deepcopy', {'iterable': iterable})
        rs = []
        for item in iterable:
            rs.append(item)

        if isinstance(iterable, tuple):
            return tuple(rs)
        elif isinstance(iterable, list):
            return rs
        elif isinstance(iterable, dict):
            return set(rs)
        elif isinstance(iterable, str):
            s = ''
            for item in rs:
                s += str(item)
            return s
        else:
            return rs

    def trunclist(self, iterable, desired):
        """Return a list with len exactly that of desired."""
        self._updhst('trunclist', {'iterable': iterable, 'desired':
                                   desired})

        if desired <= 0:
            return []

        if len(iterable) == desired:
            return iterable

        if len(iterable) < desired:
            filler = [None for n in xrange(desired-len(iterable))]
            iterable.extend(filler)
            return iterable

        if len(iterable) > desired:
            return iterable[:desired]

_functions = FunctionsWrapper()
call = _functions.call
getmodule = _functions.getmodule
getmodules = _functions.getmodules
getcommon = _functions.getcommon
deepcopy = _functions.deepcopy
trunclist = _functions.trunclist
