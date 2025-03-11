
from typing import List

import shlex

def split_command_string(cmd: str) -> List[str]:
    """
        Splits a command string into a list of tokens, handling quoted strings and escaped characters.

        :param cmd: The command string to be split.
        
        :return: A list of tokens.
    """
    
    lexer = shlex.shlex(cmd, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""

    tokens = [t for t in lexer]

    return tokens