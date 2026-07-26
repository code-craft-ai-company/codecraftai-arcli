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

# Mocking ccai.provisioning dependencies
#
# arcli deliberately does NOT depend on codecraftai-provisioning: every import
# of it is lazy, so the CLI is usable without the provisioning package
# installed.  The tests therefore have to supply it, the same way ccai.errors
# is supplied above.
#
# Only the symbols arcli's own lazy imports reach for are stubbed.  Keeping the
# stub minimal is deliberate: a broad fake would drift from the real package
# without anything noticing, and the engine itself is injected through
# enginefactory's override rather than constructed here.
if not hasattr(ccai, 'provisioning'):
    class ProvisioningAspects:
        """Stand-in carrying only the flags arcli sets."""

        def __init__(self, *, dry_run: bool = False, confirm: bool = False,
                     **kwargs):
            self.dry_run = dry_run
            self.confirm = confirm
            for name, value in kwargs.items():
                setattr(self, name, value)

    aspects_mod = types.ModuleType(
        'ccai.provisioning.aspects.provisioningaspects')
    aspects_mod.ProvisioningAspects = ProvisioningAspects

    aspects_pkg = types.ModuleType('ccai.provisioning.aspects')
    aspects_pkg.provisioningaspects = aspects_mod

    provisioning_pkg = types.ModuleType('ccai.provisioning')
    provisioning_pkg.aspects = aspects_pkg

    ccai.provisioning = provisioning_pkg
    sys.modules['ccai.provisioning'] = provisioning_pkg
    sys.modules['ccai.provisioning.aspects'] = aspects_pkg
    sys.modules['ccai.provisioning.aspects.provisioningaspects'] = aspects_mod
