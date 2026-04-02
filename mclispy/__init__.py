from importlib.resources import files

from . import lisp


core = files("mclispy").joinpath("core.lisp").read_text(encoding="utf-8")


def load_core():
    for exp in lisp.parse_all(core):
        lisp.leval(exp)


def interpret(code):
    load_core()
    return lisp.leval(lisp.parse(code))


def repl(prompt='mclis.py> '):
    load_core()
    while True:
        val = lisp.leval(lisp.parse(input(prompt)))
        if val is not None:
            print(lisp.lispstr(val))
