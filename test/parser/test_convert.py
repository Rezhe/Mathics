import unittest
import six

from mathics.core.definitions import Definitions
from mathics.core.parser import parse
from mathics.core.expression import Symbol, Integer


class ConvertTests(unittest.TestCase):
    def setUp(self):
        self.definitions = Definitions(add_builtin=True)
        self.parse = lambda code: parse(code, self.definitions)

    def parse(self, s):
        return self.parser.parse(s)

    def check(self, expr1, expr2):
        if isinstance(expr1, six.string_types):
            expr1 = self.parse(expr1)
        if isinstance(expr2, six.string_types):
            expr2 = self.parse(expr2)

        if expr1 is None:
            self.assertIsNone(expr2)
        else:
            self.assertIsTrue(expr1.same(expr2))

    def incomplete_error(self, string):
        self.assertRaises(IncompleteSyntaxError, self.parse, string)

    def invalid_error(self, string):
        self.assertRaises(InvalidSyntaxError, self.parse, string)

    def testSymbol(self):
        self.check('xX', Symbol('Global`xX'))
        self.check('context`name', Symbol('context`name'))
        self.check('`name', Symbol('Global`name'))
        self.check('`context`name', Symbol('Global`context`name'))

    def testInteger(self):
        self.check('0', Integer(0))
        self.check('1', Integer(1))
        self.check('-1', Integer(-1))

        self.check('8^^23', Integer(19))
        self.check('10*^3', Integer(10000))
        self.check('10*^-3', Rational(1, 100))
        self.check('8^^23*^2', Integer(1216))

        n = random.randint(-sys.maxsize, sys.maxsize)
        self.check(str(n), Integer(n))

        n = random.randint(sys.maxsize, sys.maxsize * sys.maxsize)
        self.check(str(n), Integer(n))

    def testString(self):
        self.check(r'"abc"', String('abc'))
        self.incomplete_error(r'"abc')
        self.check(r'"abc(*def*)"', String('abc(*def*)'))
        self.check(r'"a\"b\\c"', String(r'a"b\c'))
        self.incomplete_error(r'"\"')
        self.invalid_error(r'\""')


