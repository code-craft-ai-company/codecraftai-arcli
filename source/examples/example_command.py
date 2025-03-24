
from automojo.arcli import decorators



@decorators.option("--something")
@decorators.entry("blah")
def example_command_entry():
    return