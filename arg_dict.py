from inspect import getargspec, getcallargs
from functools import wraps


def arg_dict(func):
    argnames, _, keywords_arg, _ = getargspec(func)
    if not 'arg_dict' in argnames:
        raise Exception('this decorator requires that you accept ' +
            '"arg_dict" as a positional argument to your function')
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        try:
            callargs = getcallargs(func, *args, arg_dict={}, **kwargs)
        except TypeError: # function got multiple values for arg_dict
            i = argnames.index('arg_dict')
            before, after = args[:i], args[i:]
            args_with_dummy = before + ['arg-dict-here'] + after
            callargs = getcallargs(func, *args_with_dummy, **kwargs)

        # Check **kwargs' existence and add its contents to arg_dict
        if keywords_arg:
            kwargs_dict = callargs.pop(keywords_arg)
            callargs.update(kwargs_dict)

        callargs.pop('arg_dict')

        # call original function
        return func(arg_dict=callargs, **callargs)
    return wrapper
