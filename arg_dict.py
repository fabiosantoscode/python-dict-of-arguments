from inspect import getargspec, getcallargs
from functools import wraps


class arg_dict(object):
    def __init__(self, f):
        self.wrappee = f
        args, _, keywords, _ = getargspec(f)
        if not 'arg_dict' in args:
            raise Exception('this decorator requires that you accept '
                '"arg_dict" as an argument to your function')

    def __call__(self, *args, **kwargs):
        argnames, _, keywords, _ = getargspec(self.wrappee)

        args = list(args)
        
        try:
            arg_dict = getcallargs(self.wrappee, *args, arg_dict={}, **kwargs)
            print argnames, args
            print self.wrappee.__name__
        except TypeError: # function got multiple values for arg_dict
            i = argnames.index('arg_dict')
            args_with_dummy_argdict = args[:i] + [{}] + args[i:]
            arg_dict = getcallargs(self.wrappee, *args_with_dummy_argdict, **kwargs)

        # Check **kwargs' existence and add its contents to arg_dict
        if keywords:
            kwargs_dict = arg_dict.pop(keywords)
            arg_dict.update(kwargs_dict)

        arg_dict.pop('arg_dict')

        # call original function
        return self.wrappee(arg_dict=arg_dict, **arg_dict)

