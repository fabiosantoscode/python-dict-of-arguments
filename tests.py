from unittest import TestCase, main
from arg_dict import arg_dict

# test functions
@arg_dict
def f1(arg_dict, a, b, c=3):
    return arg_dict

@arg_dict
def f2(a, arg_dict, b, c=3, **kwargs):
    return arg_dict



class TestArgDictDecorator(TestCase):
    def test_simple(self):
        self.assertEqual(
            f1(1, 2),
            {'a': 1, 'b': 2, 'c': 3})

    def test_overriding_defaults(self):
        self.assertEqual(
            f1(1, 2, c=4),
            {'a': 1, 'b': 2, 'c': 4})

    def test_get_kwargs(self):
        self.assertEqual(
            f2(a='a', b='b', foo='bar'),
            {'a': 'a', 'b': 'b', 'c': 3, 'foo': 'bar'})
    
    def test_simultaneous(self):
        # test that several instances of the function are able to
        # run simultaneously. Examples: Recursiveness, threading,
        # generators, coroutines. Here we use a generator to test
        # this because they're very easy to control.
        @arg_dict
        def simultaneous(arg_dict, an_argument):
            yield arg_dict['an_argument']
        
        first = simultaneous('first')
        second = simultaneous('second')
        self.assertEqual(next(first), 'first')
        self.assertEqual(next(second), 'second')
    
    def test_kwargs(self):
        @arg_dict
        def with_kwargs(arg_dict, **kwargs):
            # this would be weird
            self.assertNotIn('arg_dict', arg_dict)
            return arg_dict
        self.assertEqual(
            with_kwargs(foo=1, bar=2, baz=3),
            dict(foo=1, bar=2, baz=3))

    def test_several_argument_dispositions(self):
        @arg_dict
        def as_first_arg(arg_dict, a, b):
            ret = arg_dict['a'], arg_dict['b']
            self.assertEqual(ret, (a, b))
            return ret

        self.assertEqual((1, 2),
            as_first_arg(1, 2))

        self.assertEqual((1, 2),
            as_first_arg(1, b=2))


        @arg_dict
        def as_middle_arg(a, arg_dict, b):
            ret = arg_dict['a'], arg_dict['b']
            self.assertEqual(ret, (a, b))
            return ret

        self.assertEqual((1, 2),
            as_middle_arg(1, 2))
        
        self.assertEqual((1, 2),
            as_middle_arg(1, b=2))
        
        self.assertEqual((1, 2),
            as_middle_arg(a=1, b=2))
        
        @arg_dict
        def as_last_arg(a, b, arg_dict):
            ret = arg_dict['a'], arg_dict['b']
            self.assertEqual(ret, (a, b))
            return ret

        self.assertEqual((1, 2),
            as_last_arg(1, 2))

        self.assertEqual((1, 2),
            as_last_arg(1, b=2))

        self.assertEqual((1, 2), 
            as_last_arg(a=1, b=2))

if __name__ == '__main__':
    main()
