from functools import update_wrapper
from typing import Any, Callable, Generic, TypeVar


A = TypeVar('A')


class classproperty(Generic[A]):
    """
    A read-only descriptor that turns a method into a class-level property.

    The decorated method is called with the class (not an instance) as its only
    argument, and its return value becomes the attribute value. This works both
    when accessed from the class and from instances (the instance is ignored).

    This is a minimal implementation that supports only the getter. It does not
    provide setter or deleter support. Assigning to the property on the class
    will simply overwrite the descriptor.

    Type parameter:
        A: The return type of the property getter.

    Args:
        fget (Callable[[Any], A]): A function that takes the class (type) and
            returns the computed property value. The first argument is
            conventionally named `cls`.

    Example:
        >>> class MyClass:
        ...     _base = "https://api.example.com"
        ...     @classproperty
        ...     def url(cls):
        ...         return cls._base + "/v1"
        ...
        >>> MyClass.url
        'https://api.example.com/v1'
        >>> obj = MyClass()
        >>> obj.url
        'https://api.example.com/v1'

    Note:
        The descriptor follows Python's data descriptor protocol for `__get__`,
        but lacks `__set__` and `__delete__`. As a result, class-level assignment
        (`MyClass.prop = ...`) will replace the descriptor, not call a setter.
        For writeable class properties, consider using classmethods.
    """

    def __init__(self, fget: Callable[[Any], A]) -> None:
        self.fget = fget
        self.__doc__ = fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        self.__qualname__ = getattr(fget, "__qualname__", fget.__name__)

    def __set_name__(self, owner, name):
        self.__name__ = name

    def __get__(self, instance: Any, owner: type) -> A:
        return self.fget(owner)
