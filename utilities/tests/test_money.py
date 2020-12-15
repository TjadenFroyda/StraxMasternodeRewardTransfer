import pytest
from utilities import Money


def test_create_money():
    money = Money()
    assert money == 0
    money = Money(100)
    assert money == 100


# noinspection PyTypeChecker
def test_create_money_float_raises_valueerror():
    with pytest.raises(TypeError):
        Money(10.012324)


def test_create_money_negative_raises_valueerror():
    with pytest.raises(ValueError):
        Money(-10)


# noinspection PyTypeChecker
def test_create_money_too_large_raises_valueerror():
    with pytest.raises(ValueError):
        Money(1000000000000000000)


# noinspection PyTypeChecker
def test_add_money():
    # Money + Money
    result = Money(1) + Money(3)
    assert isinstance(result, Money)
    assert result == 4
    assert Money(result) == Money(1) + Money(3)

    # Money + int
    result = Money(1) + 3
    assert isinstance(result, Money)
    assert result == 4
    assert Money(result) == Money(1) + 3

    # int + Money
    with pytest.raises(TypeError):
        3 + Money(1)

    # Money + float
    with pytest.raises(TypeError):
        Money(3) + 1.1


# noinspection PyTypeChecker
def test_subtract_money():
    # Money - Money
    result = Money(3) - Money(1)
    assert isinstance(result, Money)
    assert result == 2
    assert Money(result) == Money(3) - Money(1)

    # Money - int
    result = Money(3) - 1
    assert isinstance(result, Money)
    assert result == 2
    assert Money(result) == Money(3) - 1

    # int - Money
    with pytest.raises(TypeError):
        3 - Money(1)

    # Money - float
    with pytest.raises(TypeError):
        Money(3) - 1.1

    # Negative values
    with pytest.raises(ValueError):
        Money(1) - Money(3)


# noinspection PyStatementEffect,PyTypeChecker
def test_compare_money():
    # gt
    assert Money(3) > Money(1)
    assert Money(3) > 1
    assert not Money(1) > 3
    assert not 1 > Money(3)
    with pytest.raises(TypeError):
        Money(3) > 1.1

    # ge
    assert Money(3) >= Money(1)
    assert Money(3) >= 1
    assert Money(3) >= Money(3)
    assert Money(3) >= 3
    assert not Money(1) >= 3
    assert not 1 >= Money(3)
    with pytest.raises(TypeError):
        Money(3) >= 1.1

    # lt
    assert Money(1) < Money(3)
    assert Money(1) < 3
    assert not Money(3) < Money(1)
    assert not 3 < Money(1)
    with pytest.raises(TypeError):
        Money(3) < 3.1

    # le
    assert Money(1) <= Money(3)
    assert Money(1) <= 3
    assert Money(1) <= Money(1)
    assert Money(1) <= 1
    assert not Money(3) <= Money(1)
    assert not 3 <= Money(1)
    with pytest.raises(TypeError):
        Money(3) <= 3.1

    # eq
    assert Money(1) == Money(1)
    assert Money(1) == 1
    assert not Money(1) == Money(3)
    assert not Money(1) == 3
    with pytest.raises(TypeError):
        Money(3) == 3.1

    # ne
    assert Money(1) != Money(3)
    assert Money(1) != 3
    assert not Money(1) != Money(1)
    assert not Money(1) != 1
    with pytest.raises(TypeError):
        Money(3) != 3.1
