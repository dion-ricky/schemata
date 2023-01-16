from translator.translator import Translator
from commons.model import Schema, Schemata
from commons.exception import TranslatorTypeNotFound


class Dummy(Translator):
    """Dummy translator for exemplary and testing purposes
    
    This translator assumes all schema is NULLABLE unless
    explicitly specified with type of commons.special_type.Required.
    """

    type_mapping = {
        int: "INTEGER",
        str: "STRING",
        bool: "BOOLEAN",
        float: "FLOAT"
    }

    def get_type_mapping(self, type):
        return Dummy.type_mapping[type]

    def base_translator(self, name, type, mode="NULLABLE"):
        return {"name": name, "type": type, "mode": mode}

    def int_translator(self, schema: Schema):
        type_ = self.get_type_mapping(schema.type)
        return self.base_translator(schema.name, type_)

    def str_translator(self, schema: Schema):
        type_ = self.get_type_mapping(schema.type)
        return self.base_translator(schema.name, type_)

    def bool_translator(self, schema: Schema):
        type_ = self.get_type_mapping(schema.type)
        return self.base_translator(schema.name, type_)

    def float_translator(self, schema: Schema):
        type_ = self.get_type_mapping(schema.type)
        return self.base_translator(schema.name, type_)

    def list_translator(self, schema: Schema):
        list_type = schema.type
        schema_type = list_type.args[0]
        type_ = self.get_type_mapping(schema_type)
        return self.base_translator(schema.name, type_, "REPEATED")

    def required_translator(self, schema: Schema):
        parameterized = schema.type
        schema_type = parameterized.args[0]
        type_ = self.get_type_mapping(schema_type)
        return self.base_translator(schema.name, type_, "REQUIRED")

    def any_translator(self, schema: Schema):
        if isinstance(schema.type, Schemata):
            fields = Dummy().translate(schema.type)
            translated = self.base_translator(schema.name, "RECORD")
            translated.update({"fields": fields})
            return translated
        else:
            raise TranslatorTypeNotFound(
                f"Translator for type {str(type)} is not defined")

    def translate(self, schemata: Schemata):
        translated = []

        for schema in schemata.schemas:
            translated.append(self.translate_schema(schema))

        return translated