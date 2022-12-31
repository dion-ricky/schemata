from pytest import fixture


class TestResolveInheritance:

    @fixture
    def schemata_no_inheritance(self):

        class PureSchemata:
            id: int
            name: str

        yield PureSchemata

    @fixture
    def schemata_with_inheritance(self, schemata_no_inheritance):
        from datetime import datetime

        class SchemataInheritance(schemata_no_inheritance):
            created_date: datetime

        yield SchemataInheritance

    @fixture
    def schemata_dbl_inheritance(self, schemata_with_inheritance):
        from datetime import datetime

        class SchemataDblInheritance(schemata_with_inheritance):
            updated_date: datetime

        yield SchemataDblInheritance

    def test_no_inheritance(self, schemata_no_inheritance):
        from commons.utils import resolve_inheritance
        from commons.model import Schemata, Schema

        id = Schema('id', int)
        name = Schema('name', str)
        schemata = Schemata('PureSchemata', [id, name])

        assert resolve_inheritance(schemata_no_inheritance) == schemata

    def test_inherit_once(self, schemata_with_inheritance):
        from datetime import datetime
        from commons.utils import resolve_inheritance
        from commons.model import Schemata, Schema

        id = Schema('id', int)
        name = Schema('name', str)
        created_date = Schema('created_date', datetime)
        schemata = Schemata('SchemataInheritance', [id, name, created_date])

        assert resolve_inheritance(schemata_with_inheritance) == schemata

    def test_double_inheritance(self, schemata_dbl_inheritance):
        from datetime import datetime
        from commons.utils import resolve_inheritance
        from commons.model import Schemata, Schema

        id = Schema('id', int)
        name = Schema('name', str)
        created_date = Schema('created_date', datetime)
        updated_date = Schema('updated_date', datetime)
        schemata = Schemata('SchemataDblInheritance',
                            [id, name, created_date, updated_date])

        assert resolve_inheritance(schemata_dbl_inheritance) == schemata
