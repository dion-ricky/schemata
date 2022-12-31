from typing import _BaseGenericAlias, Any, Tuple, List

from attrs import define


@define
class ParameterizedType:
    alias: _BaseGenericAlias
    origin: Any
    args: Tuple[Any]


@define
class Schema:
    name: str
    type: Any


@define
class Schemata:
    name: str
    schemas: List[Schema]
