import importlib
import pkgutil

__all__ = []

for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if is_pkg:
        continue

    module = importlib.import_module(f".{module_name}", package=__name__)

    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if (
            isinstance(attribute, type)
            and hasattr(attribute, "revision")
            and getattr(attribute, "__module__", None) == module.__name__
        ):
            globals()[attribute_name] = attribute
            if attribute_name not in __all__:
                __all__.append(attribute_name)
