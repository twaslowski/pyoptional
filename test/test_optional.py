import pytest

from joptional import Optional  # type: ignore


def test_empty_creation() -> None:
    empty_optional = Optional.empty()
    assert empty_optional.is_present() is False


def test_get_on_empty_throws():
    empty_optional = Optional.empty()
    with pytest.raises(ValueError) as e:
        empty_optional.get()

    assert str(e.value) == "No value present"


def test_of_creation():
    optional = Optional.of("value")
    assert optional.is_present() is True
    assert optional.get() == "value"


def test_of_creation_with_none():
    with pytest.raises(ValueError) as e:
        Optional.of(None)

    assert str(e.value) == "Value may not be None"


def test_of_nullable_creation():
    optional = Optional.of_nullable(None)
    assert optional.is_present() is False


def test_equality_for_both_none():
    assert Optional.empty() == Optional.empty()


def test_equality_for_none_and_value():
    assert Optional.empty() != Optional.of(1)


def test_equality_for_values():
    assert Optional.of(1) == Optional.of(1)


def test_equality_for_complex_values():
    class SomeClass:
        def __init__(self):
            self.id = id(self)

    assert Optional.of(SomeClass()) != Optional.of(SomeClass())


def test_equality_for_non_optional():
    assert Optional.of(1) != 1


def test_if_present_with_side_effects():
    optional = Optional.of(1)
    global some_number
    some_number = 1

    def side_effect(x):
        global some_number
        some_number += x

    optional.if_present(side_effect)
    assert some_number == 2


def test_if_present_with_side_effect_for_empty_optional():
    optional = Optional.empty()
    global some_number
    some_number = 1

    def side_effect(x):
        global some_number
        some_number += x

    optional.if_present(side_effect)
    assert some_number == 1


def test_filter():
    optional = Optional.of(1)
    result = optional.filter(lambda x: x == 1)
    assert result.is_present() is True
    assert result == Optional.of(1)


def test_filter_for_none():
    optional = Optional.of(1)
    result = optional.filter(lambda x: x == 2)
    assert result == Optional.empty()


def test_filter_for_empty_optional():
    optional = Optional.empty()
    result = optional.filter(lambda x: x == 1)
    assert result == Optional.empty()


def test_map():
    optional = Optional.of(1)
    result = optional.map(lambda x: x + 1)
    assert result == Optional.of(2)


def test_map_for_none():
    optional = Optional.of(1)
    result = optional.map(lambda x: None)
    assert result == Optional.empty()


def test_map_for_empty_optional():
    optional = Optional.empty()
    result = optional.map(lambda x: x + 1)
    assert result == Optional.empty()


def test_map_for_different_types():
    optional = Optional.of(1)
    result = optional.map(lambda x: str(x))
    assert result == Optional.of("1")


def test_or_else_on_empty():
    optional = Optional[int].empty()
    assert optional.or_else(1) == 1


def test_or_else_on_value():
    optional = Optional[int].of(1)
    assert optional.or_else(2) == 1


def test_or_else_get_on_empty():
    optional = Optional[int].empty()
    assert optional.or_else_get(lambda: 1) == 1


def test_or_else_get_on_value():
    optional = Optional.of(1)
    assert optional.or_else_get(lambda: 2) == 1


def test_or_else_throw_on_empty():
    optional = Optional[int].empty()
    with pytest.raises(ValueError) as e:
        optional.or_else_throw(ValueError("No value present"))

    assert str(e.value) == "No value present"


def test_or_else_throw_on_value():
    optional = Optional.of(1)
    assert optional.or_else_throw(ValueError("No value present")) == 1


def test_require_callback():
    optional = Optional.of(1)
    with pytest.raises(ValueError) as e:
        optional.or_else_get(None)

    assert str(e.value) == "Callback function may not be None"


def test_flatmap():
    optional = Optional.of(1)
    result = optional.flatmap(lambda x: Optional.of(x + 1))
    assert result == Optional.of(2)


def test_flatmap_for_none():
    optional = Optional[int].empty()
    result = optional.flatmap(lambda x: x + 1)
    assert result == Optional.empty()
