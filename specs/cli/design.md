# AutoMojo ARCLI Framework Design

## Overview

The AutoMojo ARCLI (Code Craft AI Advanced Command Line Interface) framework is a Python package that provides a decorator-based approach to building command-line interfaces. Unlike Click, which requires adding options one at a time to command nodes, ARCLI allows for creating reusable groups of options with templated help strings that can be applied to multiple commands.

## Core Architecture

### Node Types

The framework is built around three primary node types that form a hierarchical command structure:

#### 1. Root Node (EntryCommand)
- **Purpose**: The top-level entry point for the CLI application
- **Characteristics**:
  - Inherits from `GroupingCommand`
  - Automatically detects program name from `sys.argv[0]`
  - Manages the CLI context and parsing lifecycle
  - Can contain child commands and option groups
  - Serves as the main callable entry point

#### 2. Group Node (GroupingCommand)
- **Purpose**: Intermediate nodes that can contain sub-commands
- **Characteristics**:
  - Extends base `Command` functionality
  - Can have child commands (`has_children` property)
  - Supports nested command hierarchies
  - Manages command routing to child nodes
  - Can have its own options and arguments

#### 3. Command Node (Command)
- **Purpose**: Leaf nodes that execute specific functionality
- **Characteristics**:
  - Base class for all command types
  - Contains options, arguments, and trap fields
  - Manages parameter parsing and validation
  - Executes the associated callable function
  - Cannot have child commands

### Field System

The framework uses a sophisticated field system to manage different types of command-line parameters:

#### ArgField (Arguments)
- Positional parameters that are required by default
- Support optional arguments with default values
- Type-safe parameter conversion
- Ordered processing based on position

#### OptionField (Options)
- Named parameters with short (`-f`) and long (`--flag`) forms
- Support for multiple operation modes:
  - **Simple**: Single value options
  - **Multiple**: Can be specified multiple times
  - **Counter**: Increments each time specified
- Boolean options with automatic negation flags (`--flag`/`--no-flag`)
- Required and optional options with defaults
- Group association for organized help display

#### TrapField (Trap Options)
- Special options that execute immediately and halt processing
- Typically used for help, version, or other meta-operations
- High-priority flags that bypass normal parameter flow
- Execute callback functions directly

### Parameter Type System

The framework provides a type-safe parameter conversion system:

#### Base Parameter Types
- **ParameterBase**: Generic base class with type safety
- **StringParameter**: String value conversion with quote handling
- **BooleanParameter**: Boolean conversion with multiple formats
- **IntegerParameter**: Integer value conversion
- **ListOfStringParameter**: Multiple string values
- **ListOfIntegerParameter**: Multiple integer values

#### Type Inference
- Automatic type detection based on option modes
- Counter mode defaults to `IntegerParameter`
- Multiple mode defaults to `ListOfStringParameter`
- Simple mode defaults to `StringParameter`
- Boolean flags automatically use `BooleanParameter`

### Option Groups

One of the key differentiating features of ARCLI is its option group system:

#### OptionGroup Class
- Reusable collections of related options
- Named groups for organized help display
- Template-based help strings with variable substitution
- Declarative option definitions using class attributes
- Attachment to commands via decorators

#### Template System
- Help strings can contain template variables
- Variables are filled when groups are attached to commands
- Enables context-specific help text
- Supports dynamic documentation generation

### Parsing System

The framework uses a progressive parsing approach:

#### ProgressiveOptionParser
- Processes command-line arguments in order
- Handles option parsing before argument collection
- Supports nested command structures
- Manages flag-to-option mapping
- Provides context-aware error messages

#### Parsing Flow
1. **Option Processing**: Parse all flags and their values
2. **Argument Collection**: Collect positional arguments
3. **Command Routing**: Route to child commands if present
4. **Parameter Validation**: Ensure required parameters are present
5. **Type Conversion**: Convert tokens to typed parameters
6. **Function Invocation**: Call command function with parameters

## Decorator System

The framework provides a rich set of decorators for building CLI applications:

### Command Decorators
- `@entry`: Creates root-level entry commands
- `@group`: Creates grouping commands that can contain sub-commands
- `@command`: Creates leaf command nodes

### Parameter Decorators
- `@argument`: Adds positional arguments to commands
- `@option`: Adds named options with extensive configuration
- `@trap`: Adds trap options for immediate execution

### Group Decorators
- `OptionGroup.attach()`: Applies option groups to commands with template filling

## Key Design Principles

### 1. Debuggability Over Performance
- Extensive error checking and validation
- Clear error messages with context
- Structured exception hierarchy
- Detailed parameter tracking

### 2. Readability Over Conciseness
- Explicit parameter definitions
- Clear separation of concerns
- Comprehensive type annotations
- Self-documenting code structure

### 3. Reusability and Modularity
- Option groups for shared functionality
- Template-based help system
- Composable command hierarchies
- Type-safe parameter system

### 4. Flexibility and Extensibility
- Multiple option modes (simple, multiple, counter)
- Custom parameter types
- Pluggable parsing system
- Decorator-based configuration

## Usage Patterns

### Basic Command Definition
```python
@option("--verbose", "-v", mode=OptionMode.Counter)
@option("--output", "-o", required=True)
@entry("myapp")
def main_command(context, verbose, output):
    # Command implementation
    pass
```

### Option Group Usage
```python
class CommonOptions(OptionGroup):
    name = "common"
    
    verbose = OptionField("--verbose", "-v", mode=OptionMode.Counter)
    output = OptionField("--output", "-o", help="Output to {target}")

@CommonOptions.attach(help_fill={"target": "file"})
@command("process")
def process_command(context, verbose, output):
    # Command implementation
    pass
```

### Nested Command Structure
```python
@group("database")
def db_group(context):
    pass

@command("migrate")
def migrate_command(context):
    pass

# Attach migrate to database group
db_group.add_command(migrate_command)
```

## Integration Points

### CLI Context
- `CliContext` object passed to all commands
- Provides access to global state and configuration
- Enables communication between command levels

### Error Handling
- `SemanticError` for logical validation errors
- `MissingOptionError` for required parameter validation
- Graceful error reporting with context

### Testing Integration
- Follows unittest framework conventions
- Supports automated testing of CLI functionality
- Provides clear separation for unit testing individual components

This design enables the creation of sophisticated command-line applications with reusable components, type safety, and excellent developer experience while maintaining the debuggability and readability standards required for testing tools and frameworks.