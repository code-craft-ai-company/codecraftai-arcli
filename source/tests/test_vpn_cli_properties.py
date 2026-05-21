
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple
from unittest.mock import MagicMock

# Ensure package paths
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / 'source/packages'))
sys.path.insert(0, str(repo_root))

from source.tests import setup_mocks  # noqa: F401

from hypothesis import given, strategies as st, settings, HealthCheck

from automojo.arcli import CliRunner, decorators
from automojo.arcli.commands.vpn import (
    mint_authkey_command, register_vpn_commands,
)
from automojo.arcli.commands.vpn import providerresolver


@dataclass
class FakeStatus:
    connected: bool = True
    backend_state: str = "Running"
    self_address: str = "100.64.0.1"
    hostname: str = "lab"
    tags: Optional[List[str]] = None
    provider: str = "tailscale"


def _make_root() -> Any:
    @decorators.entry("arcli")
    def main():
        return

    register_vpn_commands(root=main)
    return main


def _build_resolver(*, client: Any, control_plane: Any):
    def resolver(*, provider_name: str) -> Tuple[Any, Any]:
        return (client, control_plane)
    return resolver


class TestVpnCliProperties(unittest.TestCase):

    def setUp(self) -> None:
        self._control_plane = MagicMock()
        self._control_plane.mint_authkey.return_value = "tskey-auth-xx"
        self._control_plane.list_devices.return_value = []

        self._client = MagicMock()
        self._client.status.return_value = FakeStatus()

        providerresolver.set_provider_resolver(
            resolver=_build_resolver(client=self._client, control_plane=self._control_plane))
        return

    def tearDown(self) -> None:
        providerresolver.set_provider_resolver(resolver=None)
        return

    @given(provider=st.sampled_from(["tailscale", "twingate"]))
    @settings(max_examples=10, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_provider_option_round_trip(self, provider: str) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "peers", "--provider={}".format(provider)])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        return

    @given(tags=st.lists(
        st.text(alphabet=st.characters(blacklist_categories=("Cs",),
                                         blacklist_characters=" \t\n\r\x00=-"),
                min_size=1, max_size=8),
        min_size=1, max_size=20,
    ))
    @settings(max_examples=15, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_tag_option_collects_arbitrary_lists(self, tags: List[str]) -> None:
        self._control_plane.mint_authkey.reset_mock()
        root = _make_root()
        runner = CliRunner()
        args = ["vpn", "mint-authkey", "--provider=tailscale", "--show-secret"]
        for tg in tags:
            args.append("--tag={}".format(tg))
        result = runner.invoke(root, args=args)
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        _, kwargs = self._control_plane.mint_authkey.call_args
        self.assertEqual(kwargs["tags"], tags)
        return

    @given(ttl=st.integers(min_value=60, max_value=86400))
    @settings(max_examples=15, deadline=None,
              suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_ttl_option_accepts_integer_range(self, ttl: int) -> None:
        self._control_plane.mint_authkey.reset_mock()
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=[
            "vpn", "mint-authkey", "--provider=tailscale",
            "--ttl-seconds={}".format(ttl), "--show-secret",
        ])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        _, kwargs = self._control_plane.mint_authkey.call_args
        self.assertEqual(kwargs["ttl_seconds"], ttl)
        return


if __name__ == '__main__':
    unittest.main()
