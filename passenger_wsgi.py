import os
import sys
import importlib.util

sys.path.insert(0, os.path.dirname(__file__))

def load_source(name, pathname):
    spec = importlib.util.spec_from_file_location(name, pathname)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

wsgi = load_source('wsgi', 'app.py')

# LA CORRECCIÓN ESTÁ AQUÍ:
# Cambia 'wsgi.application' por 'wsgi.app'
application = wsgi.app