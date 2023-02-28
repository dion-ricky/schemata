import logging

from schemata.commons.model import Schema, ParameterizedType
from schemata.commons.exception import TranslatorTypeNotFound


class Translator:

    def get_schema_translator(self, schema: Schema):
        type_ = schema.type
        if isinstance(type_, ParameterizedType):
            type_ = type_.origin
        try:
            type_translator = eval(f"self.{type_.__name__.lower()}_translator")
            assert callable(type_translator)
            return type_translator
        except:
            try:
                type_translator = eval("self.any_translator")
                assert callable(type_translator)
                return type_translator
            except:
                logging.error(
                    f"Translator for type {str(type_)} is not defined")
                raise TranslatorTypeNotFound(
                    f"Translator for type {str(type_)} is not defined")

    def translate_schema(self, schema: Schema):
        return self.get_schema_translator(schema)(schema)

    def translate(self, schemata):
        raise NotImplementedError()