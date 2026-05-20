# Design

## Overview

Three `arcli` leaf commands sit under a `vpn` `GroupingCommand`:

- `vpn mint-authkey --provider <p>` — mints a short-lived auth key via
  `IVPNControlPlane.mint_authkey(...)`.
- `vpn peers --provider <p>` — lists devices via
  `IVPNControlPlane.list_devices(...)`.
- `vpn status --provider <p>` — queries the local daemon via
  `IVPNClient.status(...)`.

Every leaf is a thin wrapper that (1) resolves the configured client/control
plane for the chosen provider, (2) constructs a default `Aspects` object, (3)
calls one method on the protocol, (4) renders the returned object.  No
provider-specific code lives in the CLI.

See Also:
- `automojo-arcli/specs/cli/design.md` (root decorator/grouping architecture)
- `automojo-arcli/specs/cli-provision-commands/design.md`
- `automojo-interfaces/specs/vpn-client-protocol/design.md`
- `automojo-interfaces/specs/vpn-control-plane-protocol/design.md`

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  arcli root EntryCommand                     │
└────────────────────────────┬─────────────────────────────────┘
                             │ child
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              vpn GroupingCommand                             │
└────────────────────────────┬─────────────────────────────────┘
                             │ children
        ┌────────────────────┼──────────────────────┐
        ▼                    ▼                      ▼
   mint_authkey_cmd      peers_cmd             status_cmd
        │                    │                      │
        └──────────┬─────────┴──────────────────────┘
                   │ all three
                   ▼
              VPNProviderResolver
        (provider name → IVPNClient / IVPNControlPlane)
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   IVPNControlPlane      IVPNClient
   (mint-authkey,        (status)
    peers)
```

The `VPNProviderResolver` reads provider configuration (credentials, endpoint,
control-plane class name) from the same `landscape.yaml`-style file consumed by
`automojo-landscaping` and returns a constructed implementation instance.  The
resolver lives in `automojo-interop` (not in the CLI), keeping the CLI free of
construction logic.

---

## Subcommand Surface

| Subcommand | Options | Protocol call |
|---|---|---|
| `vpn mint-authkey` | `--provider <p>`, `--reusable / --no-reusable`, `--ephemeral / --no-ephemeral`, `--tag <t>` (multiple), `--ttl <seconds>` | `IVPNControlPlane.mint_authkey(reusable, ephemeral, tags, ttl_seconds, aspects)` |
| `vpn peers` | `--provider <p>`, `--format text\|json` | `IVPNControlPlane.list_devices(aspects)` |
| `vpn status` | `--provider <p>`, `--format text\|json` | `IVPNClient.status(aspects)` |

All three share an `OptionGroup` named `vpn_common` carrying the `--provider`
option.  `peers` and `status` additionally share `--format`.

---

## Data Model

The CLI itself defines no domain types.  It depends on:

- `IVPNClient`, `IVPNControlPlane`, `VPNStatus`, `VPNDeviceRecord` from
  `automojo-interfaces`.
- `VPNProviderResolver` from `automojo-interop` (or a near-equivalent helper
  if its home shifts during implementation).
- The arcli decorator surface from `automojo-arcli`.

Helper:

```python
def resolve_vpn_provider(*, provider_name: str) -> Tuple[Optional[IVPNClient],
                                                        Optional[IVPNControlPlane]]:
    """
        Resolves a configured (client, control_plane) pair for the named provider.

        :param provider_name: One of "tailscale" or "twingate".

        :returns: A tuple of (client_or_none, control_plane_or_none).
        :raises: ConfigurationError when the provider is not configured.
    """
```

```python
def build_default_aspects() -> Aspects: ...   # shared helper with provision CLI

def render_authkey(*, key: str) -> str: ...
def render_peers(*, devices: List[VPNDeviceRecord], fmt: str) -> str: ...
def render_status(*, status: VPNStatus, fmt: str) -> str: ...
```

Each leaf command body is approximately:

```python
@option("--provider", required=True, group="vpn_common")
@option("--format", default="text")
@command("peers")
def vpn_peers(context, provider, format):
    _, control_plane = resolve_vpn_provider(provider_name=provider)
    if control_plane is None:
        raise ConfigurationError(f"No control plane configured for {provider}")
    aspects = build_default_aspects()
    devices = control_plane.list_devices(aspects=aspects)
    rendered = render_peers(devices=devices, fmt=format)
    print(rendered)
    return 0
```

---

## Module Layout

```
source/packages/automojo/arcli/commands/vpn/
├── __init__.py
├── vpngroup.py              ← `vpn` GroupingCommand
├── mintauthkeycommand.py    ← `vpn mint-authkey`
├── peerscommand.py          ← `vpn peers`
├── statuscommand.py         ← `vpn status`
├── providerresolver.py      ← resolve_vpn_provider(...)
└── renderers.py             ← render_authkey / render_peers / render_status

source/testroots/testbase/automojo/tests/arcli/commands/vpn/
├── test_mintauthkeycommand.py
├── test_peerscommand.py
├── test_statuscommand.py
└── test_vpn_cli_properties.py     ← hypothesis property tests
```

File names follow the project standard: lowercase, no underscores, named after
the dominant class or callable.

---

## See Also

- `automojo-arcli/specs/cli/design.md`
- `automojo-arcli/specs/cli-provision-commands/design.md`
- `automojo-interfaces/specs/vpn-client-protocol/design.md`
- `automojo-interfaces/specs/vpn-control-plane-protocol/design.md`
- `automojo-interop` Tailscale and Twingate client specs

---

## Testing Strategy

Example-based unit tests cover each leaf command with the resolver replaced by
a recorder returning fake `IVPNClient` / `IVPNControlPlane` instances.  Each
test asserts:

- The expected method on the fake was called exactly once with the parsed
  options and a non-None `Aspects` instance.
- The rendered output reaches stdout.
- A missing `--provider` causes a non-zero exit code without invoking any
  provider object.
- An unknown `--provider` value causes a non-zero exit code without invoking
  any provider object.
- For `vpn peers` with the Twingate fake returning `overlay_ip=None`, the text
  renderer emits `-` for that column.

Property tests (`hypothesis`) covering Requirement 7:

- `test_provider_option_round_trip` — generates `--provider` values from
  `sampled_from(["tailscale", "twingate"])` and asserts the parser surfaces
  them unchanged on the command function's `provider` parameter.
- `test_tag_option_collects_arbitrary_lists` — generates lists of 1–20
  non-empty tag strings via `lists(text(min_size=1).filter(no_ws), …)` and
  asserts that repeating `--tag <t>` per entry produces an equal list.
- `test_ttl_option_accepts_integer_range` — generates integers in `[60,
  86400]` and asserts the parser surfaces the integer unchanged.
