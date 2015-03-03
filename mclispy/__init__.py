
import os.path

from . import lisp


core = open(os.path.join(os.path.dirname(__file__), 'core.lisp')).read()


def load_core():
    [lisp.leval(exp) for exp in lisp.parse_all(core)]


def interpret(code):
    load_core()
    return lisp.leval(lisp.parse(code))


def repl(prompt='mclis.py> '):
    load_core()
    while True:
        val = lisp.leval(lisp.parse(input(prompt)))
        if val is not None:
            print(lisp.lispstr(val))