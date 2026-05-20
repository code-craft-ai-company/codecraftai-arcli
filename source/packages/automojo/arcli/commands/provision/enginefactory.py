"""
    .. module:: enginefactory
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: A pluggable factory for constructing :class:`ProvisioningEngine`
                   instances from a parsed spec.  Tests replace ``engine_factory``
                   with a recorder.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Automation Mojo LLC"
__credits__ = []


from typing import Any, Callable, Dict, Optional


_engine_factory_override: Optional[Callable[..., Any]] = None


def set_engine_factory(*, factory: Optional[Callable[..., Any]]) -> None:
    """
        Override the engine factory used by the provision subcommands.

        :param factory: A callable taking ``spec`` keyword and returning a
                        ProvisioningEngine-shaped object, or None to restore
                        the default behaviour.
    """
    global _engine_factory_override
    _engine_factory_override = factory
    return


def build_engine(*, spec: Dict[str, Any]) -> Any:
    """
        Construct a :class:`ProvisioningEngine` for the supplied spec.

        Honours any factory installed via :func:`set_engine_factory`.

        :param spec: The parsed spec dictionary.

        :returns: A ProvisioningEngine-shaped object.
    """
    if _engine_factory_override is not None:
        engine = _engine_factory_override(spec=spec)
        rtnval = engine
        return rtnval

    from automojo.provisioning.provisioningengine import ProvisioningEngine
    from automojo.provisioning.cloudprovisionerregistry import CloudProvisionerRegistry

    registry = CloudProvisionerRegistry()
    engine = ProvisioningEngine(spec=spec, registry=registry)

    rtnval = engine
    return rtnval
