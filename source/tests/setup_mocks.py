import sys
import types
from pathlib import Path

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

import ccai

# Mocking ccai.errors dependencies
if not hasattr(ccai, 'errors'):
    err_mod = types.ModuleType('ccai.errors.exceptions')
    class SemanticError(Exception): pass
    class MissingOptionError(Exception): pass
    class AbstractMethodError(Exception): pass
    err_mod.SemanticError = SemanticError
    err_mod.MissingOptionError = MissingOptionError
    err_mod.AbstractMethodError = AbstractMethodError

    errors_pkg = types.ModuleType('ccai.errors')
    errors_pkg.exceptions = err_mod

    ccai.errors = errors_pkg
    sys.modules['ccai.errors'] = errors_pkg
    sys.modules['ccai.errors.exceptions'] = err_mod
