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
        self.curr = None

    def next(self):
        """
        returns (type, value)
        """
        if self.curr:
            res = self.curr
            self.curr = None
            return res
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

    def putback(self, t):
        assert self.curr is None
        self.curr = t

# print Add(Const(1), Var('x')).run({'x': 4})
# print TokenParser('x + y + ()').next()
#
# m = []
# p = TokenParser('1234 + -foo')
# while True:
#     t = p.next()
#     if not t[0]:
#         break
#     m.append(t)
#
# print m


def parse_expr(p):
    res = parse_term(p)
    while True:
        t = p.next()
        if not t[0]:
            return res
        if t[0] == '+':
            res2 = parse_term(p)
            res = Add(res, res2)
        if t[0] == '-':
            res2 = parse_term(p)
            res = Sub(res, res2)
        if t[0] == ')':
            p.putback(t)
            return res
    return res


def parse_unit(p):
    t = p.next()
    if t[0] == 'i':
        return Var(t[1])
    if t[0] == 'c':
        return Const(t[1])
    if t[0] == '(':
        res = parse_expr(p)
        assert p.next()[0] == ')'
        return res
    assert False


def parse_factor(p):
    t = p.next()
    if t[0] == '-':
        res = parse_unit(p)
        return Neg(res)
    p.putback(t)
    return parse_unit(p)


def parse_term(p):
    res = parse_factor(p)
    while True:
        t = p.next()
        if t[0] != '*':
            p.putback(t)
            return res
        res2 = parse_factor(p)
        res = Mul(res, res2)
    return res

p = TokenParser('a-b-c*(-4)')
t = parse_expr(p)
print t.run({'c': 4, 'a': 2, 'b': 5})