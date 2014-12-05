# -*- coding: utf-8 -*-

__author__ = 'oks'

# p = Program('x + y + (1 + 2 * z)')
# p.Run({'x'=1, 'y'=4, 'z'=0})
# print r

# Оставить программу в виде дерева


class Const(object):
    def __init__(self, value):
        self.value = value

    def run(self, context):
        return self.value


class Var(object):
    def __init__(self, name):
        self.name = name

    def run(self, context):
        return context[self.name]


class Add(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self, context):
        return self.x.run(context) + self.y.run(context)


class Sub(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self, context):
        return self.x.run(context) - self.y.run(context)


class Mul(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self, context):
        return self.x.run(context) * self.y.run(context)


class Neg(object):
    def __init__(self, x):
        self.x = x

    def run(self, context):
        return -self.x.run(context)


class TokenParser(object):
    def __init__(self, s):
        self.s = s

    def next(self):
        """
        returns (type, value)
        """
        s = self.s.lstrip()
        if not s:
            res = '', None
            n = 1
        elif s[0] in ['+', '-', '*', '(', ')']:
            res = s[0], None
            n = 1
        elif s[0].isdigit():
            n = 1
            while n < len(s) and s[n].isdigit():
                n += 1
            res = 'c', int(s[:n])
        elif s[0].isalpha():
            n = 1
            while n < len(s) and s[n].isalnum():
                n += 1
            res = 'i', s[:n]
        else:
            assert False
        self.s = s[n:]
        return res

# print Add(Const(1), Var('x')).run({'x': 4})
# print TokenParser('x + y + ()').next()

p = TokenParser('1234 + -foo')
while True:
    t = p.next()
    if not t[0]:
        break