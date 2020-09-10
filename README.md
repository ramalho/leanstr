# leanstr

This repository has the code for `LeanStr`,
proof-of-concept for a "lean" string class for Python,
using UTF-8 internally.

## What is this about

Since [PEP 393—Flexible String Representation](https://www.python.org/dev/peps/pep-0393/)
was implemented in Python 3.3, Unicode strings are stored as sequences of _cells_
that can be 1, 2, or 4 bytes wide, depending on the content of the string.

If a string has only Latin-1 characters (up to U+00FF),
then each character will be stored in a 1-byte cell.

If a string is not just Latin-1 but has characters from the Unicode
BMP—_Basic Multilingual Plane_ (up to U+FFFF),
then each and every character will be stored in a 2-byte cell.

Otherwise, each and every character will be stored in a 4-byte cell.

PEP 393 means that a long Latin-1 text can take 4x as much RAM if
it includes a single 🐜 (ant character, U+1F41C—not within the BMP).

Given the popularity of Emoji these days, it's interesting to explore the pros and cons
of storing strings as bytes encoded in UTF-8, which is how it's done in the Go language.

In UTF-8, ASCII characters use only 1 byte, and the rest of Unicode uses sequences of 2, 3, or 4 bytes,
depending on the bit width of the character's code point.
This potentially saves a lot memory when a few Emoji are used in a large Latin-1 or BMP text.

However, UTF-8 introduces significant processing costs for some operations,
because characters use different-sized byte sequences.
Random access becomes O(n)—requiring iteration
from the start or the end of the byte storage,
depending on the sign of the index.

This repo has a proof-of-concept implementing a `LeanStr` class with
`__iter__`, `__reversed__`, `__len__` and `__getitem__`.

Of course, any performance-oriented replacement for Python's
`str` class would have to be implemented in a language like C or Rust.

This is just me playing with the internals of UTF-8.

• LR 🤓
