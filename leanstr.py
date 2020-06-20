from collections import UserString
from typing import Iterator, NamedTuple, Optional, NewType, cast

Offset = NewType('Offset', int)


class OffsetWidth(NamedTuple):
    idx: Offset
    width: int


class LeanStr:
    def __init__(self, seq: str) -> None:
        self._data = seq.encode('utf8')
        self._length = -1  # for caching

    def _iter_indices(self) -> Iterator[OffsetWidth]:
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

    def _iter_indices_reverse(self) -> Iterator[OffsetWidth]:
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
        for i, width in self._iter_indices_reverse():
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
            iterator = self._iter_indices_reverse()
            step = -1
        char_index = start
        for offset_width in iterator:
            if char_index == key:
                return offset_width
            char_index += step
        return None

    def __getitem__(self, key: int) -> str:
        if isinstance(key, slice):
            raise NotImplementedError('slices not supported')
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
