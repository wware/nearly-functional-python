# nearly-functional-python

This repository contains some ideas to make Python as nearly FP as possible, with some example code.

How functional can python be? Functional languages have:
* Immutable values and variables and complex types
* Functions should not have side-effects (modifying global state, performing I/O)
* Lazy evaluation
* Tail-call optimization
* Algebraic data types

So here are some things to try.

* Immutability
  * Use [frozendict](https://pypi.org/project/frozendict/),
    [frozenlist](https://pypi.org/project/frozenlist/),
    [frozenset](https://docs.python.org/3/library/stdtypes.html?highlight=frozenset#frozenset),
    [frozen dataclass instances](https://docs.python.org/3/library/dataclasses.html#frozen-instances).
  * Maybe write a
    [pylint checker](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html#write-a-checker)
    that detects variable reassignment.
* Typing
  * Use lots of [type hints](https://docs.python.org/3/library/typing.html) with
    ["mypy –strict"](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html),
    flake8, and
    [pyright](https://github.com/microsoft/pyright)
    for linting and to approximate static typing.
  * Use Python >= 3.10 to get pattern matching and other relevant...
  * Algebraic data types ([1](https://www.gidware.com/python-adts/), [2](https://stackoverflow.com/questions/16258553))
* Iterators, lazy evaluation, etc
  * Read this [Pycon thing](https://pycon2019.trey.io/iterator-protocol.html) about lazy iterators.
  * Mess around with examples (map, filter, reduce, things I've seen done in OCaml or Haskell).
* Tail call recursion
  * [It already exists](https://pypi.org/project/tail-recursive/). I just need to whip up a few examples.
* Memoization??

## FP advocacy

[Michael Clarkson](https://www.engineering.cornell.edu/faculty-directory/michael-clarkson) is a brilliant OCaml guy at Cornell
([textbook](https://cs3110.github.io/textbook/cover.html), [videos](https://www.youtube.com/@MichaelRyanClarkson/videos))
who has done a lot of advocacy for FP. He is deeply rooted in its theory, history and underpinnings, but has a very
sensible rounded view of it. He is versed in the theory without getting lost in it. He understands why it's
important to write bullet-proof code in a world that needs a lot more bullet-proof code. He's smart and articulate
and a good writer and those videos represent a ton of work. In addition to the Cornell OCaml course he has also worked
on theorem provers, formally provable software correctness, [Coq](https://coq.inria.fr/), all that good stuff that
historically set the direction for FP.
