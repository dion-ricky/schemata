from pytest import fixture, raises


class TestTranslator:

    @fixture
    def schemata_no_dep(self):

        class PureSchemata:
            id: int
            name: str

        return PureSchemata

    @fixture
    def schemata_with_parameter(self):
        from commons.special_type import Required

        class SchemataWithParam:
            id: Required[int]
            name: str

        return SchemataWithParam

    @fixture
    def schemata_with_inheritance(self, schemata_no_dep):

        class SchemataWithInheritance(schemata_no_dep):
            description: str

        return SchemataWithInheritance

    @fixture
    def schemata_with_dep(self, schemata_no_dep):

        class SchemataWithDep:
            item: schemata_no_dep
            price: float

        return SchemataWithDep

    def test_translate_no_dep(self, schemata_no_dep):
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency

        translator = Dummy()
        schemata = resolve_dependency(schemata_no_dep)

        assert translator.translate(schemata) == [{
            "name": "id",
            "type": "INTEGER",
            "mode": "NULLABLE"
        }, {
            "name": "name",
            "type": "STRING",
            "mode": "NULLABLE"
        }]

    def test_translate_with_param(self, schemata_with_parameter):
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency

        translator = Dummy()
        schemata = resolve_dependency(schemata_with_parameter)

        assert translator.translate(schemata) == [{
            "name": "id",
            "type": "INTEGER",
            "mode": "REQUIRED"
        }, {
            "name": "name",
            "type": "STRING",
            "mode": "NULLABLE"
        }]

    def test_translate_with_inheritance(self, schemata_with_inheritance):
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency

        translator = Dummy()
        schemata = resolve_dependency(schemata_with_inheritance)

        assert translator.translate(schemata) == [{
            "name": "id",
            "type": "INTEGER",
            "mode": "NULLABLE"
        }, {
            "name": "name",
            "type": "STRING",
            "mode": "NULLABLE"
        }, {
            "name": "description",
            "type": "STRING",
            "mode": "NULLABLE"
        }]

    def test_translate_with_dep(self, schemata_with_dep):
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency

        translator = Dummy()
        schemata = resolve_dependency(schemata_with_dep)

        assert translator.translate(schemata) == [{
        "name": "item",
        "type": "RECORD",
        "mode": "NULLABLE",
        "fields": [{
                "name": "id",
                "type": "INTEGER",
                "mode": "NULLABLE"
            }, {
                "name": "name",
                "type": "STRING",
                "mode": "NULLABLE"
            }]
        }, {
            "name": "price",
            "type": "FLOAT",
            "mode": "NULLABLE"
        }]

    def test_translate_raises(self):
        from typing import Tuple
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency
        from commons.exception import TranslatorTypeNotFound

        class Schemata:
            names: Tuple[str]

        translator = Dummy()
        schemata = resolve_dependency(Schemata)

        with raises(TranslatorTypeNotFound):
            translator.translate(schemata)

    def test_translate_repeated(self):
        from typing import List
        from translator.dummy import Dummy
        from commons.utils import resolve_dependency

        class Schemata:
            names: List[str]

        translator = Dummy()
        schemata = resolve_dependency(Schemata)

        assert translator.translate(schemata) == [{
            "name": "names",
            "type": "STRING",
            "mode": "REPEATED"
        }]