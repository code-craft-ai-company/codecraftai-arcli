# Requirements

## Introduction

The `cli-vpn-commands` feature adds three `arcli` subcommands —
`vpn mint-authkey`, `vpn peers`, `vpn status` — that act as thin wrappers over
the VPN abstractions in `automojo-interfaces` (`IVPNClient`,
`IVPNControlPlane`) as implemented by `automojo-interop`'s Tailscale and
Twingate clients.  Per §1.14 of `IMPLEMENTATION-PLAN.md` and §2.9 of
`PLAN-VPN-AND-CLOUD-PROVISIONING.md`, the CLI surface contains **no business
logic**: each subcommand selects a provider implementation via `--provider` and
delegates to one method on the underlying protocol.

The subcommands follow the existing arcli decorator/grouping pattern documented
in `automojo-arcli/specs/cli/design.md` (root → `vpn` group → leaf commands).

See Also:
- `automojo-arcli/specs/cli/design.md`
- `automojo-interfaces/specs/vpn-client-protocol/requirements.md`
- `automojo-interfaces/specs/vpn-control-plane-protocol/requirements.md`

---

## Requirements

### Requirement 1: `vpn` Group Registration

**User Story:** As a CLI user, I want a `vpn` command group under the `arcli`
root so that all VPN operations live under one namespace.

#### Acceptance Criteria

1. THE SYSTEM SHALL register a `GroupingCommand` named `"vpn"` under the root
   `EntryCommand`.
2. WHEN the user invokes `arcli vpn --help` THE SYSTEM SHALL list the three leaf
   subcommands `mint-authkey`, `peers`, `status`.

---

### Requirement 2: `--provider` Selector

**User Story:** As a CLI user, I want to choose between Tailscale and Twingate
implementations with a single uniform option.

#### Acceptance Criteria

1. WHEN any leaf subcommand is invoked THE SYSTEM SHALL accept a required
   `--provider` option whose value is constrained to the set
   `{"tailscale", "twingate"}`.
2. IF `--provider` is omitted THEN THE SYSTEM SHALL exit with a non-zero exit
   code and print a `MissingOptionError` explaining the choice set.
3. IF `--provider` is set to any value outside the set THEN THE SYSTEM SHALL
   exit with a non-zero exit code and print the allowed values.

---

### Requirement 3: `vpn mint-authkey` Subcommand

**User Story:** As a CLI user, I want to mint a short-lived auth key from the
selected provider's control plane so I can paste it into a one-off bring-up
script.

#### Acceptance Criteria

1. WHEN the user invokes `arcli vpn mint-authkey --provider <p>` THE SYSTEM
   SHALL load the configured `IVPNControlPlane` for `<p>` and call
   `mint_authkey(reusable=<bool>, ephemeral=<bool>, tags=<list>,
   ttl_seconds=<int>, aspects=<default>)`.
2. THE SYSTEM SHALL accept options `--reusable / --no-reusable`,
   `--ephemeral / --no-ephemeral`, `--tag` (multiple), `--ttl` (integer
   seconds, default 900).
3. WHEN the control plane returns a key THE SYSTEM SHALL print it to stdout
   followed by a single newline and exit zero.
4. WHEN the control plane raises THE SYSTEM SHALL print the exception message
   and exit non-zero.

---

### Requirement 4: `vpn peers` Subcommand

**User Story:** As a CLI user, I want to list the devices the selected control
plane knows about so I can sanity-check a tailnet/network state.

#### Acceptance Criteria

1. WHEN the user invokes `arcli vpn peers --provider <p>` THE SYSTEM SHALL load
   the configured `IVPNControlPlane` for `<p>` and call `list_devices(aspects)`.
2. THE SYSTEM SHALL render the returned `List[VPNDeviceRecord]` as a
   human-readable table by default and as JSON when `--format json` is set.
3. WHERE the provider is `"twingate"` AND `VPNDeviceRecord.overlay_ip` is
   `None` THE SYSTEM SHALL render the field as the literal string `"-"` in the
   text format.

---

### Requirement 5: `vpn status` Subcommand

**User Story:** As a CLI user, I want to ask the local VPN client for its
current status so I can quickly verify connectivity on the host I am running
on.

#### Acceptance Criteria

1. WHEN the user invokes `arcli vpn status --provider <p>` THE SYSTEM SHALL
   load the configured `IVPNClient` for `<p>` and call `status(aspects)`.
2. THE SYSTEM SHALL render the returned `VPNStatus` (self address, peer count,
   connectivity flag) as human-readable text by default and as JSON when
   `--format json` is set.
3. WHEN no client is configured for the selected provider THE SYSTEM SHALL exit
   with a non-zero exit code and print a message naming the missing provider
   configuration.

---

### Requirement 6: No Business Logic in the CLI

**User Story:** As a maintainer, I want to be sure that the CLI layer never
makes VPN decisions itself so that all behaviour stays in `automojo-interop`.

#### Acceptance Criteria

1. THE SYSTEM SHALL implement each leaf command in 30 lines of code or fewer,
   exclusive of decorator declarations.
2. THE SYSTEM SHALL NOT issue any HTTP, CLI, or socket call directly from
   leaf-command modules — every external interaction MUST go through an
   `IVPNClient` or `IVPNControlPlane` instance.

---

### Requirement 7: Property-Tested Argument Parsing

**User Story:** As a maintainer, I want the option parser exercised across
arbitrary valid input shapes for `--provider`, `--tag`, and `--ttl`.

#### Acceptance Criteria

1. THE SYSTEM SHALL include a `hypothesis` property test that generates
   `--provider` values from `sampled_from(["tailscale", "twingate"])` and
   asserts the parser surfaces them unchanged.
2. THE SYSTEM SHALL include a `hypothesis` property test that generates lists
   of arbitrary non-empty tag strings (1–20 entries) and asserts that
   `--tag <t>` repeated for each entry produces an equal list on the command
   function's `tag` parameter.
3. THE SYSTEM SHALL include a `hypothesis` property test that generates
   integer `--ttl` values in `[60, 86400]` and asserts the parser produces the
   integer unchanged.
