from inspect import getargspec, getcallargs
from functools import wraps


def arg_dict(f):
    # the name of the "**" argument. Often "kwargs"
    name_of_kwargs = getargspec(f).keywords

    @wraps(f)
    def wrappee(*args, **kwargs):
        # getcallargs returns arguments as a dict
        wrappee.arg_dict = getcallargs(f, *args, **kwargs)

        # unless we want **kwargs as a key in this dict...
        kwargs_dict = wrappee.arg_dict.pop(name_of_kwargs, {})
        wrappee.arg_dict.update(kwargs_dict)

        # call the original function.
        return f(*args, **kwargs)

    return wrappee
