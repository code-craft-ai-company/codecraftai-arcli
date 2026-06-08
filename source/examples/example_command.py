
from typing import Optional

import sys


from ccai.arcli import decorators


@decorators.option("--some-a")
@decorators.option("--some-b", default="B")
@decorators.option("--some-c", required=False)
@decorators.entry("blah")
def example_command_entry(some_a: str, some_b: str, some_c: Optional[str]):
    print(some_a)
    print(some_b)
    print(some_c)
    return


if __name__ == "__main__":

    sys.argv.append('--some-a="A"')
    example_command_entry()
