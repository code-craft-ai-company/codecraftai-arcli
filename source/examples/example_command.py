

import sys


from automojo.arcli import decorators


@decorators.option("--some-a")
@decorators.option("--some-b")
@decorators.entry("blah")
def example_command_entry(some_a: str, some_b: str):
    print(some_a)
    print(some_b)
    return


if __name__ == "__main__":
    sys.argv.append('--some-a="A"')
    sys.argv.append('--some-b="B"')
    example_command_entry()
