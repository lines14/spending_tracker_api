import os
import json
import classutilities
from typing import Type, Any
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy.orm import class_mapper, RelationshipProperty

class DataUtils():
    @classutilities.classproperty
    def responses(cls):
        with open('../templates/responses.json', 'r', encoding='utf-8') as data:
            return type('', (object, ), json.loads(data.read()))

    @classmethod
    def dict_to_model(cls, data: dict):
        obj = cls()
        obj.__dict__.update(data)
        return obj
    
    @staticmethod
    def extract_foreign_id_as_id_in_dict(data: dict, parent_class: Type, child_class: Type) -> dict:
        fk_field = None

        for prop in class_mapper(child_class).iterate_properties:
            if isinstance(prop, RelationshipProperty) and prop.mapper.class_ == parent_class:
                fk_field = list(prop.local_columns)[0].name

                break

        if fk_field is None:
            return {}

        value = data.get(fk_field)

        if value is not None:
            return {'id': value}
        
        return {}
    
    @staticmethod
    def reversive_extract_foreign_id_as_id_in_dict(
        parent_data: dict[str, Any],
        parent_class: Type,
        child_class: Type
    ) -> dict[str, Any]:
        fk_field = None

        for prop in class_mapper(child_class).iterate_properties:
            if isinstance(prop, RelationshipProperty) and prop.mapper.class_ == parent_class:
                fk_field = list(prop.local_columns)[0].name
                print(list(prop.local_columns)[0])

                break

        if fk_field is None:
            return {}

        parent_id = parent_data.get("id")

        if parent_id is None:
            return {}

        return {fk_field: parent_id}