import json
import os
from typing import Any

import classutilities
from sqlalchemy.orm import RelationshipProperty, class_mapper

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class DataUtils:
    @classutilities.classproperty
    def responses(cls):  # noqa: N805
        with open("../templates/responses.json", encoding="utf-8") as data:
            return type("", (object,), json.loads(data.read()))

    @classmethod
    def dict_to_model(cls, data: dict):
        obj = cls()
        obj.__dict__.update(data)
        return obj

    @classmethod
    def search_foreign_field(cls, parent_class: type, child_class: type) -> str:
        for prop in class_mapper(child_class).iterate_properties:
            if isinstance(prop, RelationshipProperty) and prop.mapper.class_ == parent_class:
                foreign_field = next(iter(prop.local_columns)).name

                break

        return foreign_field

    @classmethod
    def extract_parent_foreign_id_as_id(cls, data: dict, parent_class: type, child_class: type) -> dict[str, Any]:
        foreign_field = cls.search_foreign_field(parent_class, child_class)

        if foreign_field is None:
            return {}

        value = data.get(foreign_field)

        if value is not None:
            return {"id": value}

        return {}

    @classmethod
    def extract_child_foreign_id_as_id(
        cls, parent_data: dict[str, Any], parent_class: type, child_class: type
    ) -> dict[str, Any]:
        foreign_field = cls.search_foreign_field(parent_class, child_class)

        if foreign_field is None:
            return {}

        parent_id = parent_data.get("id")

        if parent_id is None:
            return {}

        return {foreign_field: parent_id}

    @staticmethod
    def filter_search_fields(search_by: dict, model) -> dict:
        service_keys = {"relations", "keys", "with_soft_deleted", "soft_delete"}

        return {
            key: value
            for key, value in search_by.items()
            if (key in model.model_fields or key in service_keys) and value is not None
        }
