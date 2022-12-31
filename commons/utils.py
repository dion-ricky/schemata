import inspect
from typing import get_type_hints, Any, Dict

from commons.model import ParameterizedType, Schemata, Schema


def parse_schema(raw_schemata: Dict[str, Any]):
    return get_type_hints(raw_schemata)


def is_parameterized_type(type):
    try:
        type.__origin__
        return True
    except:
        return False


def explode(type_to_explode) -> ParameterizedType:
    """Explode parameterized types into their individual parts"""

    # Only types that are subclass of Generic can be parameterized
    if not is_parameterized_type(type_to_explode):
        return type_to_explode

    return ParameterizedType(type_to_explode, type_to_explode.__origin__,
                             type_to_explode.__args__)


def can_expand(type):
    try:
        rules = [
            not is_parameterized_type(type), not parse_schema(type) == {},
            not isinstance(type, ParameterizedType)
        ]
        return all(rules)
    except:
        return False


def resolve_dependency(raw_schemata) -> Schemata:
    type_hints = parse_schema(raw_schemata)
    schemata_name = raw_schemata.__name__

    schemas = []

    for sname, stype in type_hints.items():
        if is_parameterized_type(stype):
            stype = explode(stype)
            new_args = []
            for arg in stype.args:
                if can_expand(arg):
                    new_args.append(resolve_dependency(arg))
                    continue
                new_args.append(arg)
            stype.args = tuple(new_args)

        if can_expand(stype):
            stype = resolve_dependency(stype)

        schema = Schema(sname, stype)
        schemas.append(schema)

    schemata = Schemata(schemata_name, schemas)
    return schemata


resolve_inheritance = resolve_dependency