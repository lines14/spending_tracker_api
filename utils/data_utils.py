import os
import json
import classutilities
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class DataUtils():
    @classutilities.classproperty
    def responses(cls):
        with open('../templates/responses.json', 'r', encoding='utf-8') as data:
            return type('', (object, ), json.loads(data.read()))
        
    @classmethod
    def __nested_data_to_model(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        
        return obj
    
    @classmethod
    def dict_to_model(cls, dict):
        return json.loads(json.dumps(dict, ensure_ascii=False), object_hook=cls.__nested_data_to_model)