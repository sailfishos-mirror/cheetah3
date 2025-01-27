import os
import sys
import types

# Compatability definitions (inspired by six)
PY2 = sys.version_info[0] < 3
if PY2:
    # disable flake8 checks on python 3
    string_type = basestring  # noqa
    unicode = unicode  # noqa
else:
    string_type = str
    unicode = str

try:
    ModuleNotFoundError = ModuleNotFoundError
except NameError:  # Python 2.7, 3.4, 3.5
    ModuleNotFoundError = ImportError

try:
    RecursionError = RecursionError
except NameError:  # Python 2.7, 3.4
    RecursionError = RuntimeError

if PY2:
    import imp

    def load_module_from_file(base_name, module_name, filename):
        fp, pathname, description = imp.find_module(
            base_name, [os.path.dirname(filename)])
        try:
            module = imp.load_module(module_name, fp, pathname, description)
        finally:
            fp.close()
        return module

    new_module = imp.new_module
    get_suffixes = imp.get_suffixes

    def cache_from_source(path, debug_override=None):
        assert path.endswith('.py'), path
        if debug_override is None:
            debug_override = __debug__
        if debug_override:
            suffix = 'c'
        else:
            suffix = 'o'
        return path + suffix

else:
    import importlib.machinery
    import importlib.util

    def load_module_from_file(base_name, module_name, filename):
        specs = importlib.util.spec_from_file_location(module_name, filename)
        return specs.loader.load_module()

    new_module = types.ModuleType

    def get_suffixes():
        extensions = [
            (s, 'rb', 3) for s in importlib.machinery.EXTENSION_SUFFIXES
        ]
        source = [
            (s, 'r', 1) for s in importlib.machinery.SOURCE_SUFFIXES
        ]
        bytecode = [
            (s, 'rb', 2) for s in importlib.machinery.BYTECODE_SUFFIXES
        ]

        return extensions + source + bytecode

    from importlib.util import cache_from_source  # noqa: F401 unused
