from decimal import Decimal
from typing import Union
SATOSHI_CONVERSION = Decimal(1e8)


class Money:
    """A utility class for Money."""
    def __init__(self, value: Union['Money', int] = 0):
        if not isinstance(value, int) and not isinstance(value, Money):
            raise TypeError('Can only set value with Money or int.')

        self._value = self._validate(value)

    def __get__(self, instance, owner) -> int:
        return int(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __add__(self, other: Union['Money', int]) -> 'Money':
        if isinstance(other, Money):
            return self.__class__(self._value + other._value)
        elif isinstance(other, int):
            return self.__class__(self._value + other)
        else:
            raise TypeError('Arthimetic only supported with Money or int.')

    def __iadd__(self, other: Union['Money', int]) -> 'Money':
        if isinstance(other, Money):
            return self.__class__(self._value + other._value)
        elif isinstance(other, int):
            return self.__class__(self._value + other)
        else:
            raise TypeError('Arthimetic only supported with Money or int.')

    def __sub__(self, other: Union['Money', int]) -> 'Money':
        if isinstance(other, Money):
            if other._value > self._value:
                raise ValueError('Cannot subtract. Result will be negative.')
            return self.__class__(self._value - other._value)
        elif isinstance(other, int):
            if other > self._value:
                ValueError('Cannot subtract. Result will be negative.')
            return self.__class__(self._value - other)
        else:
            raise TypeError('Arthimetic only supported with Money or int.')

    def __lt__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value < other._value
        elif isinstance(other, int):
            return self._value < other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __gt__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value > other._value
        elif isinstance(other, int):
            return self._value > other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __ge__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value >= other._value
        elif isinstance(other, int):
            return self._value >= other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __le__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value <= other._value
        elif isinstance(other, int):
            return self._value <= other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __eq__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __ne__(self, other: Union['Money', int]) -> bool:
        if isinstance(other, Money):
            return self._value != other._value
        elif isinstance(other, int):
            return self._value != other
        else:
            raise TypeError('Can only compare to Money or int.')

    def __str__(self) -> str:
        return '{:.8f}'.format(Decimal(self._value) / SATOSHI_CONVERSION)

    def _validate(self, val: Union['Money', int]):
        # Convert Money to int and re-validate value.
        if isinstance(val, Money):
            val = val._value

        if not isinstance(val, int):
            raise TypeError('Money value must be int or Money')
        if val < 0:
            raise ValueError('Negative amounts not supported.')
        if val > 1.0e+17:
            raise ValueError('Invalid amount (too large).')
        return val
