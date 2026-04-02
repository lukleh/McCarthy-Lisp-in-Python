default:
    @just --list

sync:
    uv sync

test:
    uv run pytest

repl:
    uv run mclispy-repl

eval file="examples/subst.lisp":
    uv run mclispy-eval {{file}}
