from pytest import fixture


class TestUtils:

    @fixture
    def raw_schema(self):
        class RawSchema:
            id: int
            name: str
            mark_for_delete: bool
        yield RawSchema

    def test_parse_schema(self, raw_schema):
        from commons.utils import parse_schema

        assert parse_schema(raw_schema) == {
            'id': int,
            'name': str,
            'mark_for_delete': bool
        }