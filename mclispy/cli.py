from __future__ import annotations

import argparse
from pathlib import Path

import mclispy


def eval_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("lispfile", type=Path, help="File path containing Lisp code to run")
    args = parser.parse_args(argv)

    if not args.lispfile.is_file():
        print(f"file {args.lispfile} does not exist")
        return 1

    print(mclispy.interpret(args.lispfile.read_text(encoding="utf-8")))
    return 0


def repl_main() -> int:
    mclispy.repl()
    return 0
