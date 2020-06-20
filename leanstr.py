import itertools
from collections import abc
from typing import Iterator, NamedTuple, Optional, NewType, Union
from typing import overload

Offset = NewType('Offset', int)


class OffsetWidth(NamedTuple):
    idx: Offset
    width: int


class LeanStr(abc.Sequence):
    def __init__(self, seq: str) -> None:
        self._data = seq.encode('utf8')
        self._length = -1  # for caching

    def __str__(self) -> str:
        return self._data.decode('utf8')

    def _iter_indices(self) -> Iterator[OffsetWidth]:
        # this assumes UTF-8 encoding
        data = self._data
        offset = 0
        while offset < len(data):
            byte = data[offset]
            if byte < 0b11000000:
                width = 1
            elif byte < 0b11100000:
                width = 2
            elif byte < 0b11110000:
                width = 3
            else:
                width = 4
            yield OffsetWidth(Offset(offset), width)
            offset += width

    def _reversed_indices(self) -> Iterator[OffsetWidth]:
        # this assumes UTF-8 encoding
        data = self._data
        offset = -1
        width = 0
        while offset >= -len(data):
            byte = data[offset]
            if byte < 0b10000000:
                width = 1
                offset -= 1
            else:
                while 0b10000000 <= byte < 0b11000000:
                    width += 1
                    byte = data[offset]
                    offset -= 1
            yield OffsetWidth(Offset(offset + 1), width)
            width = 0

    def __iter__(self) -> Iterator[str]:
        data = self._data
        for i, width in self._iter_indices():
            yield data[i : i + width].decode('utf8')

    def __reversed__(self) -> Iterator[str]:
        data = self._data
        for i, width in self._reversed_indices():
            if width == 1:
                yield chr(data[i])
            else:
                end = i + width
                if end == 0:
                    end = len(data)
                yield data[i:end].decode('utf8')

    def __len__(self) -> int:
        if self._length >= 0:
            return self._length
        result = 0
        for i, _ in self._iter_indices():
            result += 1
        self._length = result
        return result

    def _scan(self, key: int, start: int) -> Optional[OffsetWidth]:
        if start == 0:
            iterator = self._iter_indices()
            step = 1
        else:
            iterator = self._reversed_indices()
            step = -1
        char_index = start
        for offset_width in iterator:
            if char_index == key:
                return offset_width
            char_index += step
        return None

    def _getslice(self, key: slice) -> 'LeanStr':
        # This was easy to do but a custom implementation should be faster:
        # lots of needless iteration, copying & encoding/decoding under the covers.
        try:
            iterator = itertools.islice(self, key.start, key.stop, key.step)
            return LeanStr(''.join(iterator))
        except ValueError:
            raise ValueError('start, stop, and step must be None or an'
                             ' integer: 0 <= x <= sys.maxsize.') from None

    @overload
    def __getitem__(self, i: int) -> str: ...
    @overload
    def __getitem__(self, s: slice) -> 'LeanStr': ...
    def __getitem__(self, key: Union[int, slice]) -> Union[str, 'LeanStr']:
        if isinstance(key, slice):
            return self._getslice(key)
        start = 0 if key >= 0 else -1
        result = self._scan(key, start)
        if result is None:
            raise IndexError('index out of range')
        offset, width = result
        if width == 1:
            return chr(self._data[offset])
        end = offset + width
        if end == 0:
            end = len(self._data)
        return self._data[offset:end].decode('utf8')
