
import sys


from automojo.arcli import decorators

def display_version():
    print("1.0.0")
    return

@decorators.option("--some-a")
@decorators.option("--some-b")
@decorators.trap("--version", trap_callback=display_version)
@decorators.entry("blah")
def example_command_entry(some_a: str, some_b: str):
    print(some_a)
    print(some_b)
    return


if __name__ == "__main__":

    sys.argv.append('--some-a="A"')
    sys.argv.append('--some-b="B"')
    sys.argv.append('--version')
    example_command_entry()
