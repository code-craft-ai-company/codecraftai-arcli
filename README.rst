=======================
Code Craft AI ArCli
=======================

The ``codecraftai-arcli`` package is the command-line-interface toolkit used by the CLI entry points across the ccai suite (for example ``testbase``, ``testplus``, ``am-interop``, and the per-package ``cmdtree`` subcommands). It provides a declarative model for building rich CLI trees without tying the suite to a specific external framework.

Highlights
==========

- Command hierarchy: ``Command``, ``GroupingCommand``, and ``EntryCommand`` under ``arcli/model/``.
- Typed parameters: ``ParameterBase`` subclasses for booleans, integers, strings (plus optional and list variants).
- Field descriptors: ``ArgField``, ``OptionField``, and ``TrapField``.
- Runtime plumbing: ``Parsing``, ``HelpGenerator``, ``Interact``, and ``Decorators``.
- ``CliRunner`` and ``Result`` pair under ``testing.py`` for unit-testing CLI commands.

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/`` - Package source code.
- ``source/tests/`` - ``unittest``-based tests.
- ``source/examples/`` - Example CLI definitions.
- ``specs/`` - CLI specifications and supporting documents.
- ``userguide/`` - Standards, conventions, and documentation.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-envrionment

Running Tests
=============

Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Run ``unittest`` tests:

.. code-block:: bash

   python -m unittest discover -s source/tests -p "test_*.py"

Standards and Conventions
=========================

- Naming conventions: ``userguide/10-02-naming-conventions.rst``
- Code organization: ``userguide/10-01-code-organization.rst``
- Coding standards: ``userguide/10-00-coding-standards.rst``

Additional Resources
====================

- User guide entry point: ``userguide/userguide.rst``
- CLI specifications: ``specs/cli/``
