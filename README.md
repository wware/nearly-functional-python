# nearly-functional-python

This repository contains some ideas to make Python as nearly FP as possible, with some example code.

## Principles of functional programming

### Functions as first-class objects

This has a number of implications. There are libraries for making use of them.

https://docs.python.org/3/library/functional.html

### Immutable data

Use [frozendict](https://pypi.org/project/frozendict/),
[frozenlist](https://pypi.org/project/frozenlist/),
[frozenset](https://docs.python.org/3/library/stdtypes.html?highlight=frozenset#frozenset),
[frozen pydantic classes](https://docs.pydantic.dev/usage/model_config/).

Maybe write a
[pylint checker](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html#write-a-checker)
that detects variable reassignment.

### Typing

[Here is some advice](https://github.com/microsoft/pyright/blob/main/docs/getting-started.md) on how to update
legacy code with typing hints.

Use lots of [type hints](https://docs.python.org/3/library/typing.html) with
["mypy –strict"](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html),
flake8, and [pyright](https://github.com/microsoft/pyright) for linting and to approximate static typing.

Use Python >= 3.10 to get pattern matching
([1](https://www.infoworld.com/article/3609208/how-to-use-structural-pattern-matching-in-python.html),
 [2](https://benhoyt.com/writings/python-pattern-matching/)) and also...

[Algebraic data types](https://stackoverflow.com/questions/16258553)

### Iterators, lazy evaluation, etc

A nice [Pycon thing](https://pycon2019.trey.io/iterator-protocol.html) about lazy iterators.

Mess around with examples (map, filter, reduce, things I've seen done in OCaml or Haskell).

Haskell has a GREAT lazy evaluation story, Python basically just has iterators.

I'm not super familiar with lazy evaluation but it sounds very valuable. Some things about it...
* Lazy evaluation is a technique that delays the evaluation of expressions until they are needed. This can be useful for improving performance and avoiding memory leaks.
* [Lazy evaluation](https://wiki.c2.com/?LazyEvaluation)
* [Why it's useful](https://stackoverflow.com/questions/265392/why-is-lazy-evaluation-useful)
* [More about lazy evaluation](https://academic.udayton.edu/saverioperugini/courses/cps343/lecture_notes/lazyevaluation.html)
* Maybe I'll have more to say about this when I understand it better.

### Tail call recursion

[It already exists](https://pypi.org/project/tail-recursive/). I just need to whip up a few examples.

## FP advocacy

Why am I interested in FP for Python? Because I work on a very big, very ugly legacy system written in Python 2.7. I've moved
part of the system to Python 3, which is great. But the more I read about FP and its benefits, and see them confirmed in my
own experience, the better I feel about FP.

[Michael Clarkson](https://www.engineering.cornell.edu/faculty-directory/michael-clarkson) is a brilliant OCaml guy at Cornell
([textbook](https://cs3110.github.io/textbook/cover.html), [videos](https://www.youtube.com/@MichaelRyanClarkson/videos))
who has done a lot of advocacy for FP. He is deeply rooted in its theory, history and underpinnings, but has a very
sensible rounded view of it. He is versed in the theory without getting lost in it. He understands why it's
important to write bullet-proof code in a world that needs a lot more bullet-proof code. He's smart and articulate
and a good writer and those videos represent a ton of work. In addition to the Cornell OCaml course he has also worked
on theorem provers, formally provable software correctness, [Coq](https://coq.inria.fr/), all that good stuff that
historically set the direction for FP.

## A few more random FP topics

* Currying is a technique that allows you to break down a function into functions that each take a single argument, more composable and reusable.
* Partial... *Python already does this.*
* Recursion...
* Memoization...
* Pattern matching... *Probably belongs in the `typing` area.*
* Monads are a way of structuring code that can be used to implement many of the other functional programming idioms.
  They are a powerful tool that can be used to make code more concise, elegant, and correct.
