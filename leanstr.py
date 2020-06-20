from collections import UserString
from typing import Iterator, NamedTuple


class IndexWidth(NamedTuple):
    idx: int
    width: int


class LeanStr:
    def __init__(self, seq: str):
        self.data: bytes = seq.encode('utf8')

    def _iter_indices(self) -> Iterator[IndexWidth]:
        data = self.data
        i = 0
        while i < len(data):
            byte = data[i]
            if byte < 0b11000000:
                width = 1
            elif byte < 0b11100000:
                width = 2
            elif byte < 0b11110000:
                width = 3
            else:
                width = 4
            yield IndexWidth(i, width)
            i += width

    def _iter_indices_reverse(self) -> Iterator[IndexWidth]:
        data = self.data
        i = -1
        width = 0
        while i >= -len(data):
            byte = data[i]
            if byte < 0b10000000:
                width = 1
                i -= 1
            else:
                while 0b10000000 <= byte < 0b11000000:
                    width += 1
                    byte = data[i]
                    i -= 1
            yield IndexWidth(i + 1, width)
            width = 0

    def __iter__(self) -> Iterator[str]:
        data = self.data
        for i, width in self._iter_indices():
            yield data[i : i + width].decode('utf8')

    def __len__(self):
        result = 0
        for i, _ in self._iter_indices():
            result += 1
        return result

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError('slices not supported')
        found = False
        if key >= 0:
            char_index = 0
            for i, width in self._iter_indices():
                if char_index == key:
                    found = True
                    break
                char_index += 1
        else:
            char_index = -1
            for i, width in self._iter_indices_reverse():
                if char_index == key:
                    found = True
                    break
                char_index -= 1
        if not found:
            raise IndexError('index out of range')
        if width == 1:
            return chr(self.data[i])
        return self.data[i : i + width].decode('utf8')
