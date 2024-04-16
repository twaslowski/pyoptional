from typing import Any, Union


class Optional:
    value: Union[Any, None]

    def __init__(self, value: Any):
        self.value = value

    @classmethod
    def empty(cls) -> "Optional":
        return Optional(None)

    @staticmethod
    def of(value: Any) -> "Optional":
        if value is None:
            raise ValueError("Value may not be None")
        return Optional(value)

    def is_present(self) -> bool:
        return self.value is not None

    def get(self) -> Any:
        if self.value is None:
            raise ValueError("No value present")
        return self.value
