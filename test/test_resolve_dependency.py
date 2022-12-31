from pytest import fixture


class TestResolveDependency:

    @fixture
    def schemata_no_dep(self):

        class PureSchemata:
            id: int
            name: str

        yield PureSchemata

    @fixture
    def schemata_with_parameter(self):
        from commons.special_type import Nullable

        class SchemataWithParam:
            id: int
            name: Nullable[str]

        yield SchemataWithParam

    @fixture
    def schemata_with_dep(self, schemata_no_dep):

        class SchemataWithDep:
            entity: schemata_no_dep
            price: float

        yield SchemataWithDep

    @fixture
    def schemata_with_param_and_dep(self, schemata_no_dep):
        from commons.special_type import Nullable

        class SchemataWithParamAndDep:
            entity: Nullable[schemata_no_dep]
            price: float

        yield SchemataWithParamAndDep

    def test_resolve_no_dep(self, schemata_no_dep):
        from commons.utils import resolve_dependency
        from commons.model import Schemata, Schema

        id = Schema('id', int)
        name = Schema('name', str)
        schemata = Schemata('PureSchemata', [id, name])

        assert resolve_dependency(schemata_no_dep) == schemata

    def test_resolve_with_dep(self, schemata_with_dep):
        from commons.utils import resolve_dependency
        from commons.model import Schemata, Schema

        id = Schema('id', int)
        name = Schema('name', str)
        schemata = Schemata('PureSchemata', [id, name])

        schemata_wrapper = Schema('entity', schemata)
        price = Schema('price', float)

        schemata_outer = Schemata('SchemataWithDep', [schemata_wrapper, price])

        assert resolve_dependency(schemata_with_dep) == schemata_outer

    def test_resolve_parameterized(self, schemata_with_parameter):
        from commons.utils import resolve_dependency
        from commons.model import Schemata, Schema, ParameterizedType
        from commons.special_type import Nullable

        id = Schema('id', int)
        nullable_str = ParameterizedType(Nullable[str], Nullable, (str, ))
        name = Schema('name', nullable_str)

        schemata = Schemata('SchemataWithParam', [id, name])

        assert resolve_dependency(schemata_with_parameter) == schemata

    def test_resolve_parameterized_with_dep(self, schemata_no_dep,
                                            schemata_with_param_and_dep):
        from commons.utils import resolve_dependency
        from commons.model import Schemata, Schema, ParameterizedType
        from commons.special_type import Nullable

        id = Schema('id', int)
        name = Schema('name', str)
        schemata = Schemata('PureSchemata', [id, name])

        nullable_entity = ParameterizedType(Nullable[schemata_no_dep],
                                            Nullable, (schemata, ))
        entity = Schema('entity', nullable_entity)
        price = Schema('price', float)

        schemata_outer = Schemata('SchemataWithParamAndDep', [entity, price])

        assert resolve_dependency(
            schemata_with_param_and_dep) == schemata_outer
