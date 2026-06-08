# Implementation Plan — cli-provision-commands

- [x] 1. Create the `ccai/arcli/commands/provision/` package skeleton with an
      `__init__.py` that registers the leaf modules on import.
- [x] 2. Implement `provisiongroup.py` exposing a `GroupingCommand` named
      `"provision"` and attach it to the arcli root `EntryCommand`.
- [x] 3. Implement `specloader.py` with `load_provisioning_spec(*, spec_path)`
      raising `FileNotFoundError` or `yaml.YAMLError` on bad inputs.
- [x] 4. Implement `aspectsfactory.py` with `build_default_aspects()` returning a
      CLI-friendly `Aspects` instance.
- [x] 5. Implement `renderers.py` with `render_plan`, `render_result`, and
      `render_inventory` covering both `text` and `json` formats.
- [x] 6. Implement `plancommand.py` — wires `ProvisioningEngine.plan(...)` and
      renders.
- [x] 7. Implement `applycommand.py` — wires `ProvisioningEngine.apply(...)`,
      with a `--dry-run` option that re-routes to `plan(...)`.
- [x] 8. Implement `destroycommand.py` — wires
      `ProvisioningEngine.destroy(...)`, gated by a `--yes` flag or interactive
      `y` confirmation.
- [x] 9. Implement `inventorycommand.py` — wires
      `ProvisioningEngine.inventory(...)` and renders.
- [x] 10. Add a shared `OptionGroup` named `provision_common` carrying the
       `--format` option and attach it to all four leaf commands.
- [x] 11. Add example-based unit tests for each leaf command using a
       `FakeProvisioningEngine` recorder.
- [x] 12. Add a `hypothesis` property test
       `test_spec_path_argument_accepts_arbitrary_valid_paths` covering
       Requirement 8 acceptance criterion 1.
- [x] 13. Add a `hypothesis` property test `test_format_option_round_trip`
       covering Requirement 8 acceptance criterion 2.
- [x] 14. Cross-link this spec from
       `codecraftai-provisioning/specs/provisioning-engine-pipeline/design.md`
       under its See Also section.
