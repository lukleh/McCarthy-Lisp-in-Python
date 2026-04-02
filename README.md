# McCarthy Lisp in Python

A tiny educational Lisp interpreter inspired by Paul Graham's
[Roots of Lisp](http://lib.store.yahoo.net/lib/paulgraham/jmc.ps).

This project intentionally stays close to the small original idea:

- no IO or side effects
- no sequential execution
- no numbers or arithmetic
- dynamic scope

The execution model is part of the fun:

`your code -> Lisp eval written in Lisp -> Lisp eval written in Python -> result`

## Quick start

The project now uses `uv` for environment and dependency management.

```bash
uv sync
uv run pytest
```

## Common commands

Evaluate a file:

```bash
uv run mclispy-eval subst.lisp
```

Start the REPL:

```bash
uv run mclispy-repl
```

The legacy top-level scripts still work too:

```bash
uv run python eval.py subst.lisp
uv run python repl.py
```

## justfile

If you use `just`, the common tasks are wrapped for convenience:

```bash
just sync
just test
just repl
just eval subst.lisp
```

## Project notes

- Python 3.10+ is supported.
- The package metadata, entry points, and lockfile have been updated so the repo
  behaves like a normal modern Python project.
- Debugging is still intentionally minimal. If evaluation goes wrong, this is
  still a small interpreter project, not a batteries-included tooling stack.

## Status

This is best treated as a compact interpreter experiment and reading project,
not a production Lisp implementation.
