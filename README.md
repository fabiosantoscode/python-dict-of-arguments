python-dict-of-arguments
========================

A decorator which gives you access to the arguments used to call your function (and defaults) as a dictionary.

How to use
----------

Decorate your function and add an `arg_dict` argument to it. Then you can access your function's parameters as a dict through it.


        from arg_dict import arg_dict
        
        @arg_dict
        def foo(bar, baz=3, arg_dict):
            arg_dict['bar'] += 1
            arg_dict.update({'qux': 10})
            return arg_dict



