import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, Union, overload

R = TypeVar("R")
T = TypeVar("T")


@overload
def suppress_errors(fallback: type[Exception]) -> Callable[[Callable[..., R]], Callable[..., Union[R, Exception]]]: ...
@overload
def suppress_errors(fallback: T) -> Callable[[Callable[..., R]], Callable[..., Union[R, T]]]: ...
def suppress_errors(fallback: Any) -> Callable[[Callable[..., R]], Callable[..., Union[R, Any]]]:
    """
    A decorator that suppresses exceptions raised by the wrapped function and returns
    a fallback value instead.

    Supports async functions or methods.

    Parameters:
        fallback: Determines what to return when an exception is caught.
            - Exception class (like Exception): Returns the caught exception object
            - Any other value: Returns that value when exception occurs

    Returns:
        Callable: A decorated version of the original function that returns either:
                  - The original return value, or
                  - The fallback value/exception

    Example:
    >>> @suppress_errors(Exception)
    ... def risky_op() -> int:
    ...     return 1 / 0
    >>> result = risky_op()  # Returns ZeroDivisionError

    >>> @suppress_errors(False)
    ... def safe_op() -> bool:
    ...     raise ValueError("error")
    >>> result = safe_op()  # Returns False

    Notes:
        - Only standard Python exceptions (derived from `Exception`) are caught.
        - Does not suppress `KeyboardInterrupt`, `SystemExit`, or `GeneratorExit`.
        - The decorator preserves the original function's metadata (name, docstring, etc.).
    """
    def decorator(func: Callable[..., R]) -> Callable[..., Union[R, Any]]:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Union[R, Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if fallback is Exception:
                    return e
                return fallback

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Union[R, Any]:
            try:
                return await func(*args, **kwargs)  #type: ignore
            except Exception as e:
                if fallback is Exception:
                    return e
                return fallback

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
    return decorator
