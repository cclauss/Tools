# -*- coding: utf-8 -*-
"""
A set of decorators to do stuff and things.
"""

__author__  = '671620616'
__version__ = '0.0.0'
__date__    = '%(date)'

def trace(f):
    '''Trace a call and return.
    
    Example:
    
    >>> from common_decorators import trace
    >>> @trace
    ... def foo(bar1, bar2):
    ...     print "foo: {}, {}".format(bar1, bar2)
    ... 
    >>> foo(2, 3)
    foo called with args (2, 3,), {}
    foo: 2, 3
    foo returned None
    >>> 
    '''
    def wrapped(*args, **kwargs):
        print "{} called with args {}, {}".format(f.__name__, args,
                                                  kwargs)
        ret = f(*args, **kwargs)
        print "{} returned {}".format(f.__name__, ret)
        return ret
    return wrapped

def floatify(f):
    '''Convert numeric arguments to floats before function is
    executed.
    
    Example:
    
    >>> from common_decorators import floatify
    >>> def div(a, b):
    ...     return a / b  # undecorated func for comparison
    ...
    >>> @floatify
    ... def div2(a, b):
    ...     return a / b
    ...
    >>> div(1, 2)
    0
    >>> div2(1, 2)
    0.5
    >>> @floatify
    ... def tester(*args, **kwargs):
    ...     for x in args:
    ...         print x, type(x)
    ...     for key in kwargs:
    ...         print key, type(kwargs[key])
    ...
    >>> func(1, 2, 'a', hello='world')
    1.0 <type 'float'>
    2.0 <type 'float'>
    a <type 'str'>
    hello <type 'str'>
    >>>
    '''
    
    def wrapped(*args, **kwargs):
        
        float_args = ()
        for arg in args:
            try:
                float_args += (float(arg),)
            except (TypeError, ValueError):
                float_args += (arg,)
        
        float_kwargs = {}
        for key in kwargs:
            val = kwargs[key]
            try:
                fval = float(val)
            except (TypeError, ValueError):
                fval = val
            float_kwargs.update({key: fval})
        
        return f(*float_args, **float_kwargs)
    return wrapped

class with_modules (object):
    def __init__(self, *modules):
        self.modules = modules
        self.stored = []
        for module in self.modules:
            self.stored.append(__import__(module))
    
    def __call__(self, f, *args, **kwargs):
        for m in self.modules:
            exec "{} = __import({})".format(m, m)
        
        def wrapped(f):
            return f(*args, **kwargs)
        return wrapped
