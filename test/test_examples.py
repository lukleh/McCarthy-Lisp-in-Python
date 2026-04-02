from pathlib import Path

import mclispy


EXAMPLE_RESULTS = {
    "compose.lisp": "(left (right a))",
    "eq.lisp": "t",
    "firstatom.lisp": "a",
    "flatten.lisp": "(a b c d e f)",
    "fixpoint-map.lisp": "((seen a) (seen b) (seen c))",
    "member.lisp": "t",
    "reverse.lisp": "(d c b a)",
    "subst.lisp": "(a m (a m c) d)",
}


def test_examples_evaluate_to_expected_results():
    examples_dir = Path(__file__).resolve().parent.parent / "examples"

    for filename, expected in EXAMPLE_RESULTS.items():
        result = mclispy.interpret((examples_dir / filename).read_text(encoding="utf-8"))
        assert mclispy.lisp.lispstr(result) == expected
