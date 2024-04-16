import pytest

from pyoptional import Optional  # type: ignore


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
