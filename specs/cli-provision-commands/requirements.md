# Requirements

## Introduction

The `cli-provision-commands` feature adds four `arcli` subcommands —
`provision plan`, `provision apply`, `provision destroy`, `provision inventory` —
that act as thin wrappers over `codecraftai-provisioning`'s `ProvisioningEngine`.
Per §1.14 of `IMPLEMENTATION-PLAN.md` and §2.9 of
`PLAN-VPN-AND-CLOUD-PROVISIONING.md`, the CLI surface contains **no business
logic**: each subcommand parses one positional argument (a spec YAML path), a
small set of common options, hands a parsed spec to the engine, and renders the
returned object.

The subcommands follow the existing arcli decorator/grouping pattern documented
in `codecraftai-arcli/specs/cli/design.md` (root → `provision` group → leaf
commands).

See Also:
- `codecraftai-arcli/specs/cli/design.md`
- `codecraftai-provisioning/specs/cloud-provisioner-lifecycle/requirements.md`
- `codecraftai-provisioning/specs/provisioning-engine-pipeline/requirements.md`

---

## Requirements

### Requirement 1: `provision` Group Registration

**User Story:** As a CLI user, I want a `provision` command group under the
`arcli` root so that all provisioning operations live under one namespace.

#### Acceptance Criteria

1. THE SYSTEM SHALL register a `GroupingCommand` named `"provision"` under the
   root `EntryCommand`.
2. WHEN the user invokes `arcli provision --help` THE SYSTEM SHALL list the four
   leaf subcommands `plan`, `apply`, `destroy`, `inventory`.

---

### Requirement 2: Spec Path Argument

**User Story:** As a CLI user, I want to pass the path to a spec YAML file
positionally so that the common case is one short command line.

#### Acceptance Criteria

1. WHEN any of the four subcommands is invoked THE SYSTEM SHALL accept exactly
   one required positional argument named `spec_path` of type `StringParameter`.
2. IF `spec_path` does not exist on disk THEN THE SYSTEM SHALL exit with a
   non-zero exit code and print a message identifying the missing path; THE
   SYSTEM SHALL NOT instantiate the `ProvisioningEngine`.
3. IF `spec_path` exists but does not parse as YAML THEN THE SYSTEM SHALL exit
   with a non-zero exit code and print a message naming the file and the parser
   error.

---

### Requirement 3: `provision plan` Subcommand

**User Story:** As a CLI user, I want `arcli provision plan <spec.yaml>` to
return the engine's intended actions without applying them, so I can review
changes before running `apply`.

#### Acceptance Criteria

1. WHEN the user invokes `arcli provision plan <spec.yaml>` THE SYSTEM SHALL
   call `ProvisioningEngine.plan(spec=<parsed-spec>, aspects=<default>)` and
   render the returned `ProvisioningPlan` to stdout in human-readable form.
2. WHEN the option `--format json` is supplied THE SYSTEM SHALL render the plan
   as JSON instead of the human-readable form.
3. WHEN the engine raises any exception THE SYSTEM SHALL exit with a non-zero
   exit code and print the exception message; THE SYSTEM SHALL NOT catch and
   swallow the exception silently.

---

### Requirement 4: `provision apply` Subcommand

**User Story:** As a CLI user, I want `arcli provision apply <spec.yaml>` to
realise the spec on the target venues.

#### Acceptance Criteria

1. WHEN the user invokes `arcli provision apply <spec.yaml>` THE SYSTEM SHALL
   call `ProvisioningEngine.apply(spec=<parsed-spec>, aspects=<default>)` and
   render the returned `ProvisioningResult`.
2. WHEN the option `--dry-run` is supplied THE SYSTEM SHALL invoke `plan(...)`
   instead of `apply(...)` and clearly label the output as a dry run.
3. WHEN the engine raises any exception THE SYSTEM SHALL exit with a non-zero
   exit code and print the exception message.

---

### Requirement 5: `provision destroy` Subcommand

**User Story:** As a CLI user, I want `arcli provision destroy <spec.yaml>` to
tear down the resources described in the spec.

#### Acceptance Criteria

1. WHEN the user invokes `arcli provision destroy <spec.yaml>` THE SYSTEM SHALL
   require either an interactive `y` confirmation OR a `--yes` flag before
   calling the engine.
2. WHEN confirmation is provided THE SYSTEM SHALL call
   `ProvisioningEngine.destroy(spec=<parsed-spec>, aspects=<default>)`.
3. IF confirmation is not provided THEN THE SYSTEM SHALL exit with a zero exit
   code and a message that no action was taken.

---

### Requirement 6: `provision inventory` Subcommand

**User Story:** As a CLI user, I want `arcli provision inventory <spec.yaml>` to
print the currently-known inventory for the resources in the spec.

#### Acceptance Criteria

1. WHEN the user invokes `arcli provision inventory <spec.yaml>` THE SYSTEM
   SHALL call `ProvisioningEngine.inventory(spec=<parsed-spec>,
   aspects=<default>)` and render the returned `List[ProvisionedResource]`.
2. WHEN the option `--format json` is supplied THE SYSTEM SHALL render the
   inventory as JSON.

---

### Requirement 7: No Business Logic in the CLI

**User Story:** As a maintainer, I want to be sure that the CLI layer never
makes provisioning decisions itself so that all behaviour stays in
`codecraftai-provisioning`.

#### Acceptance Criteria

1. THE SYSTEM SHALL implement each leaf command in 30 lines of code or fewer,
   exclusive of decorator declarations.
2. THE SYSTEM SHALL NOT invoke any venue-specific module from the CLI layer.
3. THE SYSTEM SHALL NOT mutate the parsed spec object before handing it to the
   engine.

---

### Requirement 8: Property-Tested Spec Path Parsing

**User Story:** As a maintainer, I want the spec-path argument parser exercised
across arbitrary valid path-shaped strings so the argument processor is robust.

#### Acceptance Criteria

1. THE SYSTEM SHALL include a `hypothesis` property test that generates
   arbitrary valid filesystem path strings (absolute and relative, with and
   without spaces, with arbitrary unicode segment names) and asserts the arcli
   argument parser routes them to the leaf command's `spec_path` parameter
   without raising.
2. THE SYSTEM SHALL include a property test that generates arbitrary `--format`
   option values from the set `{"text", "json"}` and asserts the parser
   produces the corresponding `format` parameter value.
