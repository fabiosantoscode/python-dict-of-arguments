from unittest import TestCase
from arg_dict import arg_dict

# test functions
@arg_dict
def f1(a, b, c=3):
    return f1.arg_dict

@arg_dict
def f2(a, b, c=3, **kwargs):
    return f2.arg_dict



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

