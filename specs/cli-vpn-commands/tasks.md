# Implementation Plan — cli-vpn-commands

- [x] 1. Create the `ccai/arcli/commands/vpn/` package skeleton with an
      `__init__.py` that registers the leaf modules on import.
- [x] 2. Implement `vpngroup.py` exposing a `GroupingCommand` named `"vpn"` and
      attach it to the arcli root `EntryCommand`.
- [x] 3. Implement `providerresolver.py` with `resolve_vpn_provider(*,
      provider_name)` returning a `(IVPNClient?, IVPNControlPlane?)` tuple
      and raising `ConfigurationError` on unknown providers.
- [x] 4. Reuse `build_default_aspects()` from `cli-provision-commands` (or
      promote it to a shared `ccai/arcli/commands/common/aspectsfactory.py`).
- [x] 5. Implement `renderers.py` with `render_authkey`, `render_peers`, and
      `render_status` covering both `text` and `json` formats.
- [x] 6. Implement `mintauthkeycommand.py` — wires
      `IVPNControlPlane.mint_authkey(...)` and prints the returned key.
- [x] 7. Implement `peerscommand.py` — wires
      `IVPNControlPlane.list_devices(...)`, renders the device list, and
      emits `"-"` for `None` overlay IPs under the Twingate provider in text
      format.
- [x] 8. Implement `statuscommand.py` — wires `IVPNClient.status(...)` and
      renders the status struct.
- [x] 9. Add the shared `OptionGroup` `vpn_common` carrying the `--provider`
      option and attach to all three leaf commands.
- [x] 10. Add example-based unit tests for each leaf command using a
       `FakeVPNControlPlane` / `FakeVPNClient` recorder pair.
- [x] 11. Add a `hypothesis` property test `test_provider_option_round_trip`
       covering Requirement 7 acceptance criterion 1.
- [x] 12. Add a `hypothesis` property test
       `test_tag_option_collects_arbitrary_lists` covering Requirement 7
       acceptance criterion 2.
- [x] 13. Add a `hypothesis` property test `test_ttl_option_accepts_integer_range`
       covering Requirement 7 acceptance criterion 3.
- [x] 14. Cross-link this spec from
       `codecraftai-interfaces/specs/vpn-client-protocol/design.md` and
       `codecraftai-interfaces/specs/vpn-control-plane-protocol/design.md`
       under their See Also sections.
