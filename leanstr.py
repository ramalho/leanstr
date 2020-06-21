from collections import abc
from typing import Iterator, NamedTuple, NewType, Union
from typing import overload

Offset = NewType('Offset', int)


class OffsetError(UnicodeError):
    def __init__(self, offset: Offset):
        self.offset = offset

    def __str__(self) -> str:
        return f'offset {self.offset}: trailing UTF-8 byte'


class OffsetWidth(NamedTuple):
    offset: Offset
    width: int


class LeanStr(abc.Sequence):
    def __init__(self, seq: str = '', *, data: bytes = b'') -> None:
        if seq and data:
            ValueError('please provide seq:str or data:bytes, not both')
        if seq:
            self._data = seq.encode('utf8')
        else:
            self._data = data
        self._length = -1  # for caching

    def __str__(self) -> str:
        return self._data.decode('utf8')

    def _iter_indices(self, offset: Offset = Offset(0)) -> Iterator[OffsetWidth]:
        # this assumes UTF-8 encoding
        data = self._data
        while offset < len(data):
            byte = data[offset]
            if byte < 128:
                width = 1
            elif byte < 0b11000000:
                raise OffsetError(offset)
            elif byte < 0b11100000:
                width = 2
            elif byte < 0b11110000:
                width = 3
            else:
                width = 4
            yield OffsetWidth(Offset(offset), width)
            offset = Offset(offset + width)

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

    def _scan(self, key: int, start: int, offset: Offset = Offset(0)) -> OffsetWidth:
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
        raise IndexError(f'index out of range: {key}')

    def _getslice(self, key: slice) -> 'LeanStr':
        if key.step is not None:
            raise NotImplementedError('slice step is not implemented')
        if (key.start is not None and key.start < 0) or (
            key.stop is not None and key.stop < 0
        ):
            raise ValueError('start and stop must be None or an'
                             ' integer: 0 <= x <= sys.maxsize.')
        if key.start is None:
            start_offset = Offset(0)
        else:
            start_offset, _ = self._scan(key.start, 0)
        if key.stop is None:
            return LeanStr(data=self._data[start_offset:])
        stop_offset, _ = self._scan(key.stop, 0, start_offset)
        return LeanStr(data=self._data[start_offset:stop_offset])

    @overload
    def __getitem__(self, i: int) -> str:
        ...

    @overload
    def __getitem__(self, s: slice) -> 'LeanStr':
        ...

    def __getitem__(self, key: Union[int, slice]) -> Union[str, 'LeanStr']:
        if isinstance(key, slice):
            return self._getslice(key)
        start = 0 if key >= 0 else -1
        offset, width = self._scan(key, start)
        if width == 1:
            return chr(self._data[offset])
        end = offset + width
        if end == 0:
            end = len(self._data)
        return self._data[offset:end].decode('utf8')
