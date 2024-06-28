from enum import Enum
from pathlib import Path

FILE_NAME = "lanterne_estive"
SOLUTIONS = Path("solutions")

# commands
COMPILE_CMD = "gcc -Wall -std=c99 -pedantic -Wextra -lm -o {} {}"
FORMATTING = "clang-format -style=microsoft --dry-run {}"
VALGRIND = "valgrind --leak-check=full --error-exitcode=1 ./{}"


# errors
class Errors(str, Enum):
    COMPILATION = "compilation"
    RUNTIME = "runtime"
    VALGRIND = "valgrind"
    UNBALANCED_BRACES = "unbalanced_braces"
    FORMATTING = "formatting"
    NO_RECURSION = "no_recursion"
    NO_BASE_2 = "no_base_2"
    NO_BITWISE = "no_bitwise"

MAX_POINTS = 11
BIG_ERROR = 2
SMALL_ERROR = 1
ERRORS = {
    "compilation": 4,
    "runtime": SMALL_ERROR,
    "valgrind": BIG_ERROR,
    "unbalanced_braces": SMALL_ERROR,
    "formatting": SMALL_ERROR,
    "no_recursion": SMALL_ERROR,
    "no_base_2": SMALL_ERROR,
    "no_bitwise": SMALL_ERROR,
}

RECURSIVE_FUNCTIONS = [
    "uniformColor",
    "countColors",
]