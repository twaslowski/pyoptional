from typing import Any, Union, Callable, TypeVar, Generic

T = TypeVar("T")


class Optional(Generic[T]):
    value: Union[T, None]

    def __init__(self, value: Any):
        self.value = value

    def __eq__(self, other: Any) -> bool:
        """
        From the JavaDocs:
        Indicates whether some other object is "equal to" this Optional. The other object is considered equal if:

        - it is also an Optional and;
        - both instances have no value present or;
        - the present values are "equal to" each other via equals().
        :param other: object to be compared to.
        :return: whether instances are equal.
        """
        if isinstance(other, Optional):
            return self.value == other.value
        else:
            return False

    @staticmethod
    def empty() -> "Optional[None]":
        return Optional(None)

    @staticmethod
    def of(value: Any) -> "Optional[T]":
        if value is None:
            raise ValueError("Value may not be None")
        return Optional(value)

    @staticmethod
    def of_nullable(value: Any) -> "Optional[Union[T | None]]":
        return Optional(value)

    def is_present(self) -> bool:
        return self.value is not None

    def get(self) -> T:
        if self.value is None:
            raise ValueError("No value present")
        return self.value

    def if_present(self, callback: Callable[[T], Any]) -> Any:
        """
        From the JavaDocs:
        If a value is present, invoke the specified consumer with the value, otherwise do nothing.
        :param callback: A Callback function that takes exactly self.value as a parameter.
        :return:
        """
        if self.is_present():
            # mypy apparently does not understand that typechecking has been performed beforehand
            return callback(self.value)  # type: ignore

    def filter(self, predicate: Callable[[T], bool]) -> "Optional[Union[T, None]]":
        """
        If a value is present, and the value matches the given predicate, return an Optional describing the value,
        otherwise return an empty Optional.
        :param predicate: filter function.
        :return:
        """
        if not self.is_present():
            return Optional.empty()  # type: ignore
        else:
            return self if predicate(self.value) else Optional.empty()  # type: ignore
