from typing import List, Tuple

from pytest import mark, raises  # type: ignore

from leanstr import LeanStr, OffsetWidth, Offset, OffsetError

ALAF = '\N{SAMARITAN LETTER ALAF}'
ROOK = '\N{BLACK CHESS ROOK}'
LBSA = '\N{LINEAR B SYLLABLE B008 A}'
FACE = '\N{GRINNING FACE}'


@mark.parametrize(
    'text, expected',
    [
        ('A', [OffsetWidth(offset=Offset(0), width=1)]),
        ('é', [OffsetWidth(offset=Offset(0), width=2)]),
        ('abc', [(0, 1), (1, 1), (2, 1)]),
        ('não', [(0, 1), (1, 2), (3, 1)]),
        (ALAF, [(0, 3)]),
        ('a' + ROOK + 'z', [(0, 1), (1, 3), (4, 1)]),
        (LBSA, [(0, 4)]),
        ('a' + FACE + 'z', [(0, 1), (1, 4), (5, 1)]),
        ('', []),
        (
            'éphéméréité',
            [
                (0, 2),
                (2, 1),
                (3, 1),
                (4, 2),
                (6, 1),
                (7, 2),
                (9, 1),
                (10, 2),
                (12, 1),
                (13, 1),
                (14, 2),
            ],
        ),
    ],
)
def test_iter_indices(text: str, expected: List[Tuple[int, int]]) -> None:
    result = list(LeanStr(text)._iter_indices())
    assert result == expected


@mark.parametrize('text, offset, expected', [
        ('éphéméréité', 0, [
                (0, 2), (2, 1), (3, 1), (4, 2), (6, 1), (7, 2),
                (9, 1), (10, 2), (12, 1), (13, 1), (14, 2)]),
        ('éphéméréité', 10, [(10, 2), (12, 1), (13, 1), (14, 2)]),
        ('éphéméréité', 14, [(14, 2)]),
    ],
)
def test_iter_indices_offset(
    text: str, offset: int, expected: List[Tuple[int, int]]
) -> None:
    result = list(LeanStr(text)._iter_indices(Offset(offset)))
    assert result == expected


def test_iter_indices_offset_error() -> None:
    with raises(OffsetError, match='offset 15: trailing UTF-8 byte'):
        print(list(LeanStr('éphéméréité')._iter_indices(Offset(15))))


@mark.parametrize('text, expected', [
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


@mark.parametrize('text, index', [
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
    'text, index', [('ace', 3), ('ace', -4), ('', 0)]
)
def test_getitem_out_of_range(text: str, index: int) -> None:
    with raises(IndexError, match='index out of range'):
        print(LeanStr(text)[index])


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_reversed(text: str) -> None:
    result = list(reversed(LeanStr(text)))
    assert result == list(reversed(text))


@mark.parametrize('text, start, stop', [
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
    assert text[start:stop] == str(result)


@mark.parametrize('start, stop', [(-3, -1), (-3, None), (None, -3)])
def test_getitem_slice_negatives_not_supported(start: int, stop: int) -> None:
    with raises(ValueError, match='start and stop must be None or an integer'):
        print(LeanStr('whatever')[-3:-1])


def test_getitem_slice_step() -> None:
    with raises(NotImplementedError, match='slice step is not implemented'):
        print(LeanStr('whatever')[::3])
