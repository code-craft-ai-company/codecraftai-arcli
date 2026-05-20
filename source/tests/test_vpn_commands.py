
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

from automojo.arcli import CliRunner, decorators
from automojo.arcli.commands.vpn import (
    mint_authkey_command,
    peers_command,
    status_command,
    register_vpn_commands,
)
from automojo.arcli.commands.vpn import providerresolver


@dataclass
class FakeDevice:
    device_id: str
    hostname: str
    overlay_address: Optional[str]
    tags: List[str]
    os: str
    last_seen: str


@dataclass
class FakeStatus:
    connected: bool
    backend_state: str
    self_address: str
    hostname: str
    tags: List[str]
    provider: str


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


class TestVpnCommands(unittest.TestCase):

    def setUp(self) -> None:
        self._client = MagicMock()
        self._client.status.return_value = FakeStatus(
            connected=True, backend_state="Running",
            self_address="100.64.0.1", hostname="lab-host",
            tags=["tag:lab"], provider="tailscale",
        )

        self._control_plane = MagicMock()
        self._control_plane.mint_authkey.return_value = "tskey-auth-xxxx"
        self._control_plane.list_devices.return_value = [
            FakeDevice(device_id="d1", hostname="hostA",
                       overlay_address="100.64.0.2",
                       tags=["tag:lab"], os="linux",
                       last_seen="2026-05-19T00:00:00Z"),
        ]

        providerresolver.set_provider_resolver(
            resolver=_build_resolver(client=self._client, control_plane=self._control_plane))
        return

    def tearDown(self) -> None:
        providerresolver.set_provider_resolver(resolver=None)
        return

    # -- mint-authkey --------------------------------------------------------

    def test_mint_authkey_returns_key(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=[
            "vpn", "mint-authkey", "--provider=tailscale",
            "--tag=tag:lab", "--ttl-seconds=900",
        ])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._control_plane.mint_authkey.call_count, 1)
        _, kwargs = self._control_plane.mint_authkey.call_args
        self.assertEqual(kwargs["ttl_seconds"], 900)
        self.assertEqual(kwargs["tags"], ["tag:lab"])
        self.assertTrue(kwargs["ephemeral"])
        self.assertIn("tskey-auth-xxxx", result.stdout)
        self.assertNotIn("WARNING", result.stdout)
        return

    def test_mint_authkey_non_ephemeral_warns(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=[
            "vpn", "mint-authkey", "--provider=tailscale", "--no-ephemeral",
        ])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertIn("WARNING", result.stdout)
        return

    def test_mint_authkey_unknown_provider_rejected(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=[
            "vpn", "mint-authkey", "--provider=wireguard",
        ])
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(self._control_plane.mint_authkey.call_count, 0)
        return

    # -- peers ---------------------------------------------------------------

    def test_peers_text_format(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "peers", "--provider=tailscale"])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._control_plane.list_devices.call_count, 1)
        self.assertIn("hostA", result.stdout)
        self.assertIn("100.64.0.2", result.stdout)
        return

    def test_peers_json_format(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "peers", "--provider=tailscale", "--format=json"])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        import json
        parsed = json.loads(result.stdout.strip())
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["hostname"], "hostA")
        return

    def test_peers_overlay_none_renders_dash(self) -> None:
        self._control_plane.list_devices.return_value = [
            FakeDevice(device_id="d2", hostname="hostB",
                       overlay_address=None, tags=[],
                       os="linux", last_seen="2026-05-19T00:00:00Z"),
        ]
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "peers", "--provider=twingate"])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        # there should be a "-" placeholder rather than the literal "None"
        self.assertIn("hostB", result.stdout)
        self.assertNotIn("None", result.stdout)
        return

    # -- status --------------------------------------------------------------

    def test_status_text(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "status", "--provider=tailscale"])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        self.assertEqual(self._client.status.call_count, 1)
        self.assertIn("100.64.0.1", result.stdout)
        self.assertIn("Running", result.stdout)
        return

    def test_status_json(self) -> None:
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "status", "--provider=tailscale", "--format=json"])
        self.assertEqual(result.exit_code, 0, msg=result.stderr)
        import json
        parsed = json.loads(result.stdout.strip())
        self.assertTrue(parsed["connected"])
        return

    def test_status_no_client_configured(self) -> None:
        providerresolver.set_provider_resolver(
            resolver=_build_resolver(client=None, control_plane=self._control_plane))
        root = _make_root()
        runner = CliRunner()
        result = runner.invoke(root, args=["vpn", "status", "--provider=tailscale"])
        self.assertNotEqual(result.exit_code, 0)
        return


if __name__ == '__main__':
    unittest.main()
