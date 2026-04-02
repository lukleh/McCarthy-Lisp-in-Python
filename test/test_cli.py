from pathlib import Path

from mclispy.cli import eval_main


def test_eval_main_prints_lisp_syntax(tmp_path, capsys):
    program = tmp_path / "program.lisp"
    program.write_text("(cons 'a '(b c))", encoding="utf-8")

    assert eval_main([str(program)]) == 0
    assert capsys.readouterr().out == "(a b c)\n"
