from typing import Any, Type, TypeVar, Generic, Union, overload

T = TypeVar('T')

class ConstantAttrib(Generic[T]):
    """
    A descriptor that enforces constant values at instance level.
    (Does not support class-level assignment)

    Example:
    >>> class MyClass:
    ...     VALUE = ConstantAttrib[int]()
    ...
    >>> obj = MyClass()
    >>> obj.VALUE = 42  # First assignment works
    >>> obj.VALUE = 10  # Raises AttributeError
    >>> print(obj.VALUE)  # 42
    """

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name
        self.private_name = f"_{name}_constant"

    @overload
    def __get__(self, instance: None, owner: Type[Any]) -> 'ConstantAttrib[T]': ...
    @overload
    def __get__(self, instance: Any, owner: Type[Any]) -> T: ...
    def __get__(self, instance: Any, owner: Type[Any]) -> Union[T, "ConstantAttrib[T]"]:
        if instance is None:
            return self

        if self.private_name not in instance.__dict__:
            raise AttributeError(f"Constant attribute '{self.name}' not set")

        return instance.__dict__[self.private_name]

    def __set__(self, instance: Any, value: T) -> None:
        if self.private_name in instance.__dict__:
            raise AttributeError(f"Cannot modify constant attribute '{self.name}'")
        instance.__dict__[self.private_name] = value

    def __delete__(self, instance: Any) -> None:
        raise AttributeError(f"Cannot delete constant attribute '{self.name}'")
