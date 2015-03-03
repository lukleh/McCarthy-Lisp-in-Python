# -*- coding: utf8 -*-

import pytest

from mclispy.lisp import parse, tokenize, Atom


def test_tokenizer():
    assert tokenize('()') == ['(', ')']
    assert tokenize("(')") == ['(', "'", ')']
    assert tokenize('   (   )      ') == ['(', ')']
    assert tokenize('   ( 1 2 )      ') == ['(', '1', '2', ')']
    assert tokenize('a b') == ['a', 'b']
    assert tokenize('((() a) b)') == ['(', '(', '(', ')', 'a', ')', 'b', ')']
    assert tokenize('(quote a)') == ['(', 'quote', 'a', ')']
    

def test_parser():
    assert parse('(quote (a b c))') == [Atom('quote'), [Atom('a'), Atom('b'), Atom('c')]]
    assert parse('(quote a))') == [Atom('quote'), Atom('a')]
    assert parse('()') == []
    assert parse('())') == []
    pytest.raises(Exception, parse, '(quote (a b c)')
    pytest.raises(Exception, parse, ')')

    assert parse("(crd '(a b c))") == [Atom('crd'), [Atom('quote'), [Atom('a'), Atom('b'), Atom('c')]]]
    assert parse("(eq 'a 'a)") == [Atom('eq'), [Atom('quote'), Atom('a')], [Atom('quote'), Atom('a')]]