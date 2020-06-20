# leanstr

This repository has the code for `LeanStr`,
proof-of-concept for a "lean" string class for Python,
using UTF-8 internally.

## What is this about

Since [PEP 393 -- Flexible String Representation](https://www.python.org/dev/peps/pep-0393/)
was implemented in Python 3.3, Unicode strings are stored as sequences of _cells_
that can be 1, 2, or 4 bytes wide, depending on the content of the string.

If a string has only Latin-1 characters (up to U+00FF),
then every character will be stored in a 1-byte cell.

If a string is not just Latin-1 but has only characters in the Unicode
_Basic Multilingual Plane (BMP)_ (up to U+FFF),
then every character will be stored in a 2-byte cell.

Otherwise, every character will be stored in a 4-byte cell.

This means that a long text in Latin-1 can use 4x the RAM if a
single 🐜 (ant character, U+1F41C) is placed in the text.

Given the popularity of Emoji these days, it's interesting to explore the pros and cons
of storing strings as bytes encoded in UTF-8, which is how it's done in the Go language.

In UTF-8, each character is stored in a sequence of 1, 2, 3, or 4 bytes,
depending on the bit width of its codepoint.

This potentially saves a lot memory when Emoji are used, but introduces
processing costs, because characters use different-sized byte sequences.
Random access becomes O(n)—requiring iterating
from the start or the end of the byte storage, depending on the sign of the index.

This repo has a proof-of-concept implementing a `LeanStr` class with
`__iter__`, `__reversed__`, `__len__` and `__getitem__`.
