# Design

## Overview

Four `arcli` leaf commands sit under a `provision` `GroupingCommand`:

- `provision plan <spec.yaml>` — dry-run, prints intended actions
- `provision apply <spec.yaml>` — apply spec
- `provision destroy <spec.yaml>` — tear down resources
- `provision inventory <spec.yaml>` — print known inventory

Every leaf is a thin wrapper that (1) parses the YAML spec, (2) constructs a
default `Aspects` object, (3) calls one method on `ProvisioningEngine`, (4)
renders the returned object.  No venue-specific code lives in the CLI.

See Also:
- `automojo-arcli/specs/cli/design.md` (root decorator/grouping architecture)
- `automojo-provisioning/specs/provisioning-engine-pipeline/design.md`
- `automojo-provisioning/specs/cloud-provisioner-lifecycle/design.md`

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  arcli root EntryCommand                     │
└────────────────────────────┬─────────────────────────────────┘
                             │ child
                             ▼
┌──────────────────────────────────────────────────────────────┐
│            provision GroupingCommand                         │
└────────────────────────────┬─────────────────────────────────┘
                             │ children
       ┌───────────┬─────────┴──────────┬────────────┐
       ▼           ▼                    ▼            ▼
   plan_cmd    apply_cmd           destroy_cmd  inventory_cmd
       │           │                    │            │
       └───────────┴────────────┬───────┴────────────┘
                                │ all four
                                ▼
                       _load_spec(spec_path)
                                │
                                ▼
                       ProvisioningEngine
                  .plan / .apply / .destroy / .inventory
                                │
                                ▼
                            renderers
                 (text or json depending on --format)
```

---

## Subcommand Surface

| Subcommand | Positional | Options | Engine call |
|---|---|---|---|
| `provision plan <spec.yaml>` | `spec_path` | `--format text\|json` | `engine.plan(spec, aspects)` |
| `provision apply <spec.yaml>` | `spec_path` | `--dry-run`, `--format text\|json` | `engine.apply(spec, aspects)` (or `plan` when `--dry-run`) |
| `provision destroy <spec.yaml>` | `spec_path` | `--yes`, `--format text\|json` | `engine.destroy(spec, aspects)` |
| `provision inventory <spec.yaml>` | `spec_path` | `--format text\|json` | `engine.inventory(spec, aspects)` |

All four use a shared `OptionGroup` named `provision_common` carrying
`--format` so help output is consistent.

---

## Data Model

The CLI itself defines no domain types.  It depends on:

- `ProvisioningEngine` (constructor + four lifecycle methods) from
  `automojo-provisioning`.
- `ProvisioningSpec`, `ProvisioningPlan`, `ProvisioningResult`,
  `ProvisionedResource` data classes (return types) from the same package.
- The arcli decorator surface (`@entry`, `@group`, `@command`, `@argument`,
  `@option`) from `automojo-arcli`.

Helper module:

```python
def load_provisioning_spec(*, spec_path: str) -> ProvisioningSpec:
    """
        Loads a provisioning spec from a YAML file.

        :param spec_path: Absolute or relative path to a YAML spec file.

        :returns: A parsed ProvisioningSpec.
        :raises: FileNotFoundError, yaml.YAMLError, ConfigurationError
    """
```

```python
def build_default_aspects() -> Aspects:
    """
        Builds the default Aspects object used by the CLI for engine calls.

        :returns: A default Aspects instance with CLI-friendly timeouts.
    """
```

```python
def render_plan(*, plan: ProvisioningPlan, fmt: str) -> str: ...
def render_result(*, result: ProvisioningResult, fmt: str) -> str: ...
def render_inventory(*, items: List[ProvisionedResource], fmt: str) -> str: ...
```

Each leaf command body is essentially:

```python
@argument("spec_path")
@option("--format", default="text", group="provision_common")
@command("plan")
def provision_plan(context, spec_path, format):
    spec = load_provisioning_spec(spec_path=spec_path)
    aspects = build_default_aspects()
    engine = ProvisioningEngine()
    plan = engine.plan(spec=spec, aspects=aspects)
    rendered = render_plan(plan=plan, fmt=format)
    print(rendered)
    return 0
```

---

## Module Layout

```
source/packages/automojo/arcli/commands/provision/
├── __init__.py
├── provisiongroup.py        ← `provision` GroupingCommand
├── plancommand.py           ← `provision plan`
├── applycommand.py          ← `provision apply`
├── destroycommand.py        ← `provision destroy`
├── inventorycommand.py      ← `provision inventory`
├── speclloader.py           ← load_provisioning_spec(...)
├── aspectsfactory.py        ← build_default_aspects()
└── renderers.py             ← render_plan / render_result / render_inventory

source/testroots/testbase/automojo/tests/arcli/commands/provision/
├── test_plancommand.py
├── test_applycommand.py
├── test_destroycommand.py
├── test_inventorycommand.py
└── test_provision_cli_properties.py     ← hypothesis property tests
```

File names follow the project standard: lowercase, no underscores, named after
the dominant class or callable.

---

## See Also

- `automojo-arcli/specs/cli/design.md`
- `automojo-arcli/specs/cli-vpn-commands/design.md`
- `automojo-provisioning/specs/provisioning-engine-pipeline/design.md`
- `automojo-provisioning/specs/cloud-provisioner-lifecycle/design.md`

---

## Testing Strategy

Example-based unit tests cover each leaf command with the engine replaced by a
`FakeProvisioningEngine` recorder.  Each test asserts:

- The expected method on the fake engine was called exactly once with the
  parsed spec and a non-None `Aspects` instance.
- The rendered output reaches stdout.
- A missing file path causes exit code != 0 without invoking the engine.
- A malformed YAML file causes exit code != 0 without invoking the engine.
- `destroy` exits with code 0 and prints "no action taken" when the `--yes`
  flag is absent and stdin is not a TTY.

Property tests (`hypothesis`) covering Requirement 8:

- `test_spec_path_argument_accepts_arbitrary_valid_paths` — generates path
  strings using `hypothesis.strategies.text(...)` filtered to omit NULs and
  path separators within segments, joins segments with `os.sep`, prepends both
  absolute and relative roots, and asserts arcli parses each as the leaf
  command's `spec_path` argument.  The test stops short of dereferencing the
  file (a `FileNotFoundError` is the expected next step but lives outside the
  argument parser).
- `test_format_option_round_trip` — generates `--format` values from
  `sampled_from(["text", "json"])` and asserts the parser surfaces the value
  unchanged on the command function's `format` parameter.
