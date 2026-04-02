# McCarthy Lisp in Python

A tiny educational Lisp interpreter inspired by Paul Graham's
[Roots of Lisp](https://paulgraham.com/rootsoflisp.html).

This project intentionally stays close to the small original idea:

- no IO or side effects
- no sequential execution
- no numbers or arithmetic
- dynamic scope

The execution model is part of the fun:

`your code -> Lisp eval written in Lisp -> Lisp eval written in Python -> result`

## Supported language

This interpreter supports the tiny symbolic Lisp used in the McCarthy /
Graham "Roots of Lisp" lineage:

- atoms and proper lists
- quote syntax with both `quote` and `'`
- the primitive forms `atom`, `eq`, `car`, `cdr`, `cons`, `cond`, `lambda`,
  and `label`
- dynamic scope

The bundled core library adds a few useful definitions on top of that:

- `null`
- `and`
- `not`
- `append`
- `pair`
- `assoc`
- `eval`

What it does not support is just as important:

- no numbers or arithmetic
- no strings
- no macros
- no side effects or IO
- no sequential execution forms
- no comments syntax

## Quick start

The project now uses `uv` for environment and dependency management.

```bash
uv sync
uv run pytest
```

## Common commands

Evaluate a file:

```bash
uv run mclispy-eval examples/subst.lisp
```

Start the REPL:

```bash
uv run mclispy-repl
```

The legacy top-level scripts still work too:

```bash
uv run python eval.py examples/subst.lisp
uv run python repl.py
```

## justfile

If you use `just`, the common tasks are wrapped for convenience:

```bash
just sync
just test
just repl
just eval examples/subst.lisp
```

## Example programs

Runnable example programs live in [`examples/`](/home/lukas/projects/McCarthy-Lisp-in-Python/examples).

- `examples/eq.lisp`: smallest smoke test
- `examples/subst.lisp`: the meta-circular substitution example
- `examples/firstatom.lisp`: recursively find the leftmost atom in a nested list
- `examples/reverse.lisp`: reverse a flat symbolic list
- `examples/member.lisp`: test symbolic membership in a list
- `examples/flatten.lisp`: flatten a nested symbolic list
- `examples/compose.lisp`: compose two anonymous functions and apply the result
- `examples/fixpoint-map.lisp`: a Y-combinator-style example using an
  applicative-order fixed-point combinator to build `map` without `label`

## Project notes

- Python 3.10+ is supported.
- The package metadata, entry points, and lockfile have been updated so the repo
  behaves like a normal modern Python project.
- Debugging is still intentionally minimal. If evaluation goes wrong, this is
  still a small interpreter project, not a batteries-included tooling stack.

## Status

This is best treated as a compact interpreter experiment and reading project,
not a production Lisp implementation.
