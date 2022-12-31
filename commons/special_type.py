from typing import Generic, TypeVar

T = TypeVar('T')


class DummySpecialType(Generic[T]):
    """This is an example of how to define a special type.
    
    This type accepts ONE parameter with type of T. To use
    this special type you can write "DummySpecialType[str]"
    and substitute 'str' with any type that you want.

    To create special types with multiple parameters, create
    another TypeVar for example "V = TypeVar('V')" and use
    it in the Generic base class of the special type.
    For example "DummySpecialType(Generic[T, V])".
    """
    pass


class Nullable(Generic[T]):
    pass


class Required(Generic[T]):
    pass


class PII_HIGH(Generic[T]):
    pass


class PII_LOW(Generic[T]):
    pass