# -*- coding: utf8 -*-

import pytest

import mclispy
from mclispy.lisp import parse, leval, Atom, global_env, parse_all


@pytest.fixture(scope='module')
def core():
    return [leval(exp) for exp in parse_all(mclispy.core)]


def test_quote():
    assert leval(parse('(quote a)')) == Atom('a')
    assert leval(parse('(quote ())')) == []
    assert leval(parse('(quote (a b c))')) == [Atom('a'), Atom('b'), Atom('c')]


def test_atom():
    assert leval(parse('(atom (quote a))')) == Atom('t')
    assert leval(parse("(atom 'a)")) == Atom('t')
    assert leval(parse("(atom '(a b c))")) == []
    assert leval(parse("(atom '())")) == Atom('t')
    assert leval(parse("(atom (atom 'a))")) == Atom('t')
    assert leval(parse("(atom '(atom 'a))")) == []


def test_eq():
    assert leval(parse('(eq (quote a) (quote a))')) == Atom('t')
    assert leval(parse("(eq 'a 'a)")) == Atom('t')
    assert leval(parse('(eq (quote a) (quote b))')) == []
    assert leval(parse('(eq (quote ()) (quote ()))')) == Atom('t')


def test_car():
    assert leval(parse('(car (quote (a b c)))')) == Atom('a')


def test_cdr():
    assert leval(parse('(cdr (quote (a b c)))')) == [Atom('b'), Atom('c')]


def test_cons():
    assert leval(parse('(cons (quote a) (quote (b c)))')) == [Atom('a'), Atom('b'), Atom('c')]
    assert leval(parse('(cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))')) == [Atom('a'),
                                                                                             Atom('b'),
                                                                                             Atom('c')]
    assert leval(parse('(car (cons (quote a) (quote (b c))))')) == Atom('a')
    assert leval(parse('(cdr (cons (quote a) (quote (b c))))')) == [Atom('b'), Atom('c')]
    assert leval(parse("(cons '(h a) (quote (b c)))")) == [[Atom('h'), Atom('a')], Atom('b'), Atom('c')]
    assert leval(parse("(cons 'a '())")) == [Atom('a')]


def test_cond():
    assert leval(parse("""(cond
                            ((eq (quote a) (quote b)) (quote first))
                            ((atom (quote a)) (quote second)))""")) == Atom('second')


def test_lambda():
    assert leval(parse("((lambda (x) (cons x '(b))) 'a)")) == [Atom('a'), Atom('b')]
    assert leval(parse("""(
                            (lambda (x y) (cons x (cdr y)))
                            'z '(a b c)
                            )"""
    )) == [Atom('z'), Atom('b'), Atom('c')]
    assert leval(parse("""(
                            (lambda (f) (f '(b c)))
                            '(lambda (x) (cons 'a x))
                            )"""
    )) == [Atom('a'), Atom('b'), Atom('c')]


def test_label():
    leval(parse("""(label subst (lambda (x y z)
                                        (cond ((atom z)
                                               (cond ((eq z y) x)
                                                     ('t z)))
                                              ('t (cons (subst x y (car z))
                                                        (subst x y (cdr z)))))))
                           """))
    assert global_env[Atom('subst')]

    p = leval(parse("""(subst 'm 'b '(a b (a b c) d))"""))
    assert p == [Atom('a'), Atom('m'), [Atom('a'), Atom('m'), Atom('c')], Atom('d')]

    p = leval(parse("""((label subst (lambda (x y z)
                                        (cond ((atom z)
                                               (cond ((eq z y) x)
                                                     ('t z)))
                                              ('t (cons (subst x y (car z))
                                                        (subst x y (cdr z)))))))
                        'm 'b '(a b (a b c) d))
                           """))
    assert p == [Atom('a'), Atom('m'), [Atom('a'), Atom('m'), Atom('c')], Atom('d')]


def test_core(core):
    assert leval(parse("(null 'a)")) == []
    assert leval(parse("(null '())")) == Atom('t')

    assert leval(parse("(and (atom 'a) (eq 'a 'a))")) == Atom('t')
    assert leval(parse("(and (atom 'a) (eq 'a 'b))")) == []

    assert leval(parse("(not (eq 'a 'a))")) == []
    assert leval(parse("(not (eq 'a 'b))")) == Atom('t')

    assert leval(parse("(append '(a b) '(c d))")) == [Atom('a'), Atom('b'), Atom('c'), Atom('d')]
    assert leval(parse("(append '() '(c d))")) == [Atom('c'), Atom('d')]

    assert leval(parse("(pair '() '())")) == []
    assert leval(parse("(pair '(x) '(a))")) == [[Atom('x'), Atom('a')]]
    assert leval(parse("(pair '(x y z) '(a b c))")) == [[Atom('x'), Atom('a')],
                                                        [Atom('y'), Atom('b')],
                                                        [Atom('z'), Atom('c')]]

    assert leval(parse("(assoc 'x '((x a) (y b)))")) == Atom('a')
    assert leval(parse("(assoc 'x '((x new) (x a) (y b)))")) == Atom('new')


def test_eval(core):
    assert leval(parse("(eval 'x '((x a) (y b)))")) == Atom('a')
    assert leval(parse("(eval '(eq 'a 'a) '())")) == Atom('t')
    assert leval(parse("(eval '(cons x '(b c)) '((x a) (y b)))")) == [Atom('a'), Atom('b'), Atom('c')]
    assert leval(parse("(eval '(cond ((atom x) 'atom) ('t 'list)) '((x '(a b))))")) == Atom('list')
    assert leval(parse("(eval '(f '(b c)) '((f (lambda (x) (cons 'a x)))))")) == [Atom('a'), Atom('b'), Atom('c')]
    assert leval(parse("""(eval '((label firstatom (lambda (x)
                                                    (cond ((atom x) x)
                                                          ('t (firstatom (car x))))))
                                  y)
                                '((y ((a b) (c d)))))""")) == Atom('a')

