================================================================
AutoMojo ARCLI (Advanced Reusable Command-Line Interface)
================================================================

The AutoMojo ARCLI framework is a Python package that provides a decorator-based approach to building command-line interfaces. Unlike Click, which requires adding options one at a time to command nodes, ARCLI allows for creating reusable groups of options with templated help strings that can be applied to multiple commands.

Features
========
- **Reusable Option Groups:** Define common options once and attach them to many commands.
- **Templated Help Strings:** Dynamically render help text depending on the context of the command.
- **Three-Tier Command Hierarchy:** Easily organize commands into `workspace`, `collection`, and `action` tiers for clarity and structure.
- **Decorator-Driven:** Clean, declarative syntax to construct the CLI tree.

Installation
============
Using Poetry:

.. code-block:: bash

    poetry add automojo-arcli

Usage
=====
ARCLI is built on top of standard CLI parsing paradigms but drastically reduces boilerplate when standardizing common arguments across a suite of tools.

.. code-block:: python

    from automojo.arcli import command, option_group

    @option_group("database_options")
    def db_options():
        pass
    
    @command("query")
    @db_options.attach()
    def run_query():
        pass

Development
===========
This repository provides a standard Poetry environment. 

1. Setup the machine environment:
   Run `repository-setup/setup-ubuntu-machine` (if applicable)

2. Activate virtual environment:
   Run `poetry shell` and `poetry install`

References
==========
- `User Guide <userguide/userguide.rst>`
- `Coding Standards <userguide/10-00-coding-standards.rst>`
