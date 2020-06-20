from typing import List, Tuple

from pytest import mark, raises  # type: ignore

from leanstr import LeanStr

ALAF = '\N{SAMARITAN LETTER ALAF}'
ROOK = '\N{BLACK CHESS ROOK}'
LBSA = '\N{LINEAR B SYLLABLE B008 A}'
FACE = '\N{GRINNING FACE}'


@mark.parametrize(
    'text, expected',
    [
        ('A', [(0, 1)]),
        ('é', [(0, 2)]),
        ('abc', [(0, 1), (1, 1), (2, 1)]),
        ('não', [(0, 1), (1, 2), (3, 1)]),
        (ALAF, [(0, 3)]),
        ('a' + ROOK + 'z', [(0, 1), (1, 3), (4, 1)]),
        (LBSA, [(0, 4)]),
        ('a' + FACE + 'z', [(0, 1), (1, 4), (5, 1)]),
        ('', []),
    ],
)
def test_iter_indices(text: str, expected: List[Tuple[int, int]]) -> None:
    result = list(LeanStr(text)._iter_indices())
    assert result == expected


@mark.parametrize(
    'text, expected',
    [
        ('A', [(-1, 1)]),
        ('é', [(-2, 2)]),
        ('abc', [(-1, 1), (-2, 1), (-3, 1)]),
        ('não', [(-1, 1), (-3, 2), (-4, 1)]),
        (ALAF, [(-3, 3)]),
        ('a' + ROOK + 'z', [(-1, 1), (-4, 3), (-5, 1)]),
        (LBSA, [(-4, 4)]),
        ('a' + FACE + 'z', [(-1, 1), (-5, 4), (-6, 1)]),
        ('', []),
    ],
)
def test_iter_reversed_indices(text: str, expected: List[int]) -> None:
    result = list(LeanStr(text)._reversed_indices())
    assert result == expected


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_iter(text: str) -> None:
    result = list(LeanStr(text))
    assert result == list(text)


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_len(text: str) -> None:
    my_str = LeanStr(text)
    result = len(my_str)
    # test cache
    my_str._data = bytes()
    result2 = len(my_str)
    assert result == len(text)
    assert result == result2


@mark.parametrize(
    'text, index',
    [
        ('Šedivý', 0),
        ('Šedivý', 1),
        ('Šedivý', 2),
        ('Šedivý', 3),
        ('Šedivý', -1),
        ('Šedivý', -2),
        ('Šedivý', -3),
        ('Šedivý', -4),
    ],
)
def test_getitem(text: str, index: int) -> None:
    result = LeanStr(text)[index]
    assert result == text[index]

@mark.parametrize(
    'text, index', [('ace', 3), ('ace', -4), ('', 0),],
)
def test_getitem_out_of_range(text: str, index: int) -> None:
    with raises(IndexError, match='index out of range'):
        print(LeanStr(text)[index])

@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_reversed(text: str) -> None:
    result = list(reversed(LeanStr(text)))
    assert result == list(reversed(text))


@mark.parametrize(
    'text, start, stop', 
    [
        ('Šedivý', 1, 3),
        ('Šedivý', 1, 3),
        ('Šedivý', None, 3),
        ('Šedivý', 2, None),
        ('Šedivý', 2, 2),
        ('Šedivý', 2, 1),
    ],
)
def test_getitem_slice_positive_start_stop(text: str, start: int, stop: int) -> None:
    result = LeanStr(text)[start:stop]
    assert str(result) == text[start:stop]


@mark.parametrize(
    'start, stop', 
    [
        (-3, -1),
        (-3, None),
        (None, -3),
    ],
)
def test_getitem_slice_negatives_not_supported(start: int, stop: int) -> None:
    with raises(ValueError, match='start, stop, and step must be None or an integer'):
        print(LeanStr('whatever')[-3:-1])

