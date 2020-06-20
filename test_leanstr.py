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
def test_iter_indices(text, expected) -> None:
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
def test_iter_indices_reverse(text, expected) -> None:
    result = list(LeanStr(text)._iter_indices_reverse())
    assert result == expected


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_iter(text) -> None:
    result = list(LeanStr(text))
    assert result == list(text)


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_len(text) -> None:
    my_str = LeanStr(text)
    result = len(my_str)
    # test cache
    my_str._data = bytes() 
    result2 = len(my_str)  # test cache
    assert result == len(text)
    assert result == result2


@mark.parametrize(
    'text, index',
    [
        ('ação', 0),
        ('ação', 1),
        ('ação', 2),
        ('ação', 3),
        ('ação', -1),
        ('ação', -2),
        ('ação', -3),
        ('ação', -4),
        ('axé', -1),
    ],
)
def test_get_char(text, index) -> None:
    result = LeanStr(text)[index]
    assert result == text[index]


@mark.parametrize(
    'text, index', [('ace', 3), ('ace', -4), ('', 0),],
)
def test_get_char_out_of_range(text, index) -> None:
    with raises(IndexError, match='index out of range'):
        print(LeanStr(text)[index])


@mark.parametrize('text', ['A', 'abc', 'não', ALAF, LBSA, ROOK + FACE, ''])
def test_reversed(text) -> None:
    result = list(reversed(LeanStr(text)))
    assert result == list(reversed(text))
