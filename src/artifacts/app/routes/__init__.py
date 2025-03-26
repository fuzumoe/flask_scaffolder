# app/routes/__init__.py

import importlib
import pkgutil
from flask_restx import Api
from app import routes  # reference to the app.routes package


def register_routes(api: Api) -> None:
    """Auto-imports and registers all route modules with `namespace` and `path` defined."""

    # Iterate over all modules in app.routes
    for _, module_name, is_pkg in pkgutil.iter_modules(routes.__path__):
        if is_pkg:
            continue  # Skip sub-packages if any

        module_full_name = f"{routes.__name__}.{module_name}"

        try:
            module = importlib.import_module(module_full_name)

            # Only register if both `namespace` and `path` exist
            if hasattr(module, "namespace") and hasattr(module, "path"):
                api.add_namespace(module.namespace, path=module.path)

        except Exception as e:
            print(f"Failed to load module {module_full_name}: {e}")
