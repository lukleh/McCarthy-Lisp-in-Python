from importlib.resources import files

from . import lisp


core = files("mclispy").joinpath("core.lisp").read_text(encoding="utf-8")


def load_core(env=None):
    if env is None:
        env = lisp.global_env

    for exp in lisp.parse_all(core):
        lisp.leval(exp, env)

    return env


def interpret(code):
    env = load_core({})
    return lisp.leval(lisp.parse(code), env)


def repl(prompt='mclis.py> '):
    env = load_core({})
    while True:
        val = lisp.leval(lisp.parse(input(prompt)), env)
        if val is not None:
            print(lisp.lispstr(val))
