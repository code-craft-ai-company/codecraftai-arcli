import importlib.util
import sys
import types
from pathlib import Path


def _importable(dotted_name: str) -> bool:
    """
        True when ``dotted_name`` can be imported from the current sys.path.

        ``importlib.util.find_spec`` imports the PARENT packages of a dotted
        name, so probing 'ccai.provisioning.aspects.x' raises
        ModuleNotFoundError when 'ccai.provisioning' itself is absent -- the
        very case the probe is meant to detect.  Walk the name one segment
        at a time instead.

        A name that is already loaded (a real module or a stub installed by
        :func:`install_mocks`) counts as importable; stub modules carry no
        ``__spec__``, which ``find_spec`` would reject.
    """
    if dotted_name in sys.modules:
        return True

    parts = dotted_name.split(".")
    for depth in range(1, len(parts) + 1):
        try:
            if importlib.util.find_spec(".".join(parts[:depth])) is None:
                return False
        except ModuleNotFoundError:
            return False
    return True

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

import ccai

def install_mocks() -> None:
    """
        Installs stand-in modules for the ``ccai.errors`` and ``ccai.provisioning`` packages when the real packages
        cannot be imported.  Safe to call more than once: once a stub is installed its module name is loaded, so
        the probe reports it as importable and nothing is installed twice.
    """
    # Mocking ccai.errors dependencies
    #
    # Stub ONLY when the real package cannot be imported.  ``hasattr(ccai,
    # 'errors')`` is the wrong probe: before anything imports the subpackage the
    # attribute is absent even when codecraftai-foundations is installed, and the
    # stub then shadows the real package for every later import in the process --
    # ccai.testbase, for one, needs ccai.errors.xtraceback and fails with
    # "'ccai.errors' is not a package".
    if not _importable("ccai.errors.exceptions"):
        err_mod = types.ModuleType('ccai.errors.exceptions')
        # Mirror the real contract: ccai.errors.exceptions.SemanticError derives
        # from BaseException ON PURPOSE so misuse halts a run even under a broad
        # 'except Exception'.  A stub that derives from Exception changes what the
        # tests observe (CliRunner would swallow it), so keep the stub faithful.
        class SemanticError(BaseException): pass
        class MissingOptionError(SemanticError): pass
        class AbstractMethodError(SemanticError): pass
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
    if not _importable("ccai.provisioning.aspects.provisioningaspects"):
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

    return


install_mocks()
