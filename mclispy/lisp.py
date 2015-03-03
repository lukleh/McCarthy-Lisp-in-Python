# -*- coding: utf8 -*-

import re


def parse(code):
    return read_from_tokens(tokenize(code))


def parse_all(code):
    tokens = tokenize(code)
    while tokens:
        yield read_from_tokens(tokens)


def tokenize(chars):
    return [item for t in chars.replace('(', ' ( ').replace(')', ' ) ').split() for item in re.split("(')", t) if item]


def read_from_tokens(tokens, depth=0):
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while True:
            if not tokens:
                raise Exception('unexpected program end - missing parentheses?')
            if tokens[0] == ')':
                break
            L.append(read_from_tokens(tokens, depth=depth+1))
        if L:
            L2 = []
            q = False
            for a in L:
                if a == Atom("'"):
                    L2.append([Atom('quote')])
                    q = True
                else:
                    if q:
                        L2[-1].append(a)
                        q = False
                    else:
                        L2.append(a)
            L = L2
        tokens.pop(0)
        return L
    elif ')' == token and depth < 1:
        raise Exception('unexpected )')
    else:
        if depth == 0:
            raise Exception('no form found')
        return Atom(token)


class Atom():
    def __init__(self, a):
        self.a = a

    def __eq__(self, other):
        return isinstance(other, Atom) and self.a == other.a

    def __hash__(self):
        return hash(self.a)

    def __str__(self):
        return self.a

    def __repr__(self):
        return self.__str__()


global_env = {}


def leval(x, env=global_env):

    if isinstance(x, Atom):
        # print('ATOM', x, env[x])
        return env[x]

    if not isinstance(x, list):
        raise Exception('list expected')
    # print('LIST', x)
    # print('ENVs', len(env))
    # for k, v in env.items():
    #     if str(k) in ['eval', 'not', 'assoc', 'evlis', 'null', 'pair', 'append', 'and', 'evcon']:
    #         continue
    #     print('==', k, ':', v)
    operator = x[0]

    if operator == Atom('quote'):
        (_, exp) = x
        return exp
    elif operator == Atom('atom'):
        (_, exp) = x
        value = leval(exp, env)
        if not isinstance(value, list) or value == []:
            return Atom('t')
        else:
            return []
    elif operator == Atom('eq'):
        args = [leval(arg, env) for arg in x[1:]]
        assert len(args) == 2
        if args[0] == args[1]:
            return Atom('t')
        else:
            return []
    elif operator == Atom('car'):
        assert len(x) == 2
        args = leval(x[1], env)
        return args[0]
    elif operator == Atom('cdr'):
        assert len(x) == 2
        args = leval(x[1], env)
        return args[1:]
    elif operator == Atom('cons'):
        args = [leval(arg, env) for arg in x[1:]]
        assert len(args) == 2
        assert isinstance(args[1], list)
        return [args[0]] + args[1]
    elif operator == Atom('cond'):
        for arg in x[1:]:
            assert isinstance(arg, list)
            assert len(arg) == 2
            p = leval(arg[0], env)
            if p == Atom('t'):
                return leval(arg[1], env)
        else:
            raise Exception('cond: no condition met')
    elif operator == Atom('lambda'):
        assert len(x) == 3
        assert isinstance(x[1], list)
        assert isinstance(x[2], list)
        params = x[1]
        body = x[2]
        return Procedure(params, body, env)
    elif operator == Atom('label'):
        l = x[1]
        f = x[2]
        v = leval(f, env)
        env[l] = v
        return v
    elif isinstance(operator, Atom):
        return leval([env[operator]] + x[1:], env)
    elif isinstance(operator, Procedure):
        args = [leval(arg, env) for arg in x[1:]]
        return operator(*args)
    else:
        proc = leval(operator, env)
        args = [leval(arg, env) for arg in x[1:]]
        return proc(*args)


def lispstr(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        env = self.env.copy()
        env.update(zip(self.parms, args))
        return leval(self.body, env)

    def __str__(self):
        return 'LAMBDA %s' % self.body

    def __repr__(self):
        return self.__str__()
