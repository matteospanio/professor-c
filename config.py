from enum import Enum
from pathlib import Path

FILE_NAME = "percorsi"
SOLUTIONS = Path("solutions")

# commands
COMPILE_CMD = "gcc -Wall -std=c99 -pedantic -Wextra -lm -o {} {}"
FORMATTING = "clang-format -style=microsoft --dry-run {}"
VALGRIND = "valgrind --leak-check=full --error-exitcode=1 ./{}"

# errors
MAX_POINTS = 11
BIG_ERROR = 2
SMALL_ERROR = 1

class Errors(int, Enum):
    COMPILATION = BIG_ERROR
    RUNTIME = SMALL_ERROR
    VALGRIND = SMALL_ERROR
    UNBALANCED_BRACES = SMALL_ERROR
    NO_RECURSION = SMALL_ERROR
    NO_BASE_2 = SMALL_ERROR
    NO_BITWISE = SMALL_ERROR

RECURSIVE_FUNCTIONS = [
    "budgetTravel"
]
