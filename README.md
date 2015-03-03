### Original McCarthy Lisp in Python

Original in the sense of Paul Graham's [Roots of Lisp](http://lib.store.yahoo.net/lib/paulgraham/jmc.ps).

That means:

* no IO (no side-effects)
* no sequential excecution
* no numbers or arithmetics
* dynamic scope

Python interprets Lisp code which itself then interprets Lisp eval in Lisp :)

That is: [your code] -> [lisp eval in lisp] -> [lisp eval in python] -> [result]

Requires Python3

Really non-existent debugging. If something goes wrong, you can only wonder.

#### Usage

Evaluate:
``python eval.py subst.lisp``

Repl:
``python repl.py``