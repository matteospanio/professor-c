#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
import subprocess
import sys

from rich.logging import RichHandler

import rules

logging.basicConfig(
    format="%(message)s",
    datefmt="[%X]",
    level="NOTSET",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger(__name__)

FILE_NAME = "lanterne_estive"

SOLUTIONS = pathlib.Path(__file__).parent / "solutions"
COMPILE_CMD = "gcc -Wall -std=c99 -pedantic -Wextra -lm -o {} {}"
FORMATTING = "clang-format -style=microsoft --dry-run {}"
VALGRIND = "valgrind --leak-check=full --error-exitcode=1 ./{}"


def check_formatting(solution: pathlib.Path):
    res = True
    result = subprocess.run(
        FORMATTING.format(solution), shell=True, capture_output=True
    )
    if result.stderr:
        res = False
        with open(f"logs/{solution.parent.stem}.log", "+a") as f:
            f.write("\n## Formatting issues:\n")
            f.write(result.stderr.decode())

    return res


def check_runtime(solution: pathlib.Path):
    res = 0
    result = subprocess.run(f"./{FILE_NAME}", shell=True, capture_output=True)
    if result.returncode != 0:
        res = -1
        with open(f"logs/{solution.parent.stem}.log", "+a") as f:
            f.write("\n## Runtime error:\n")
            f.write(result.stderr.decode())

    if "Tutti i test sono passati!" not in str(result.stdout):
        res = 1

    return res


def check_compilation(solution: pathlib.Path):
    res = True
    result = subprocess.run(
        COMPILE_CMD.format(FILE_NAME, solution), shell=True, capture_output=True
    )
    out = result.stderr.decode()
    if result.returncode != 0:
        res = False
        with open(f"logs/{solution.parent.stem}.log", "+a") as f:
            f.write("\n## Compilation error:\n")
            f.write(out)

    if "warning" in out:
        log.warning(f"{solution.parent.stem} compiled with warning")

    return res


def check_valgrind(solution: pathlib.Path):
    res = True
    result = subprocess.run(VALGRIND.format(FILE_NAME), shell=True, capture_output=True)
    if result.returncode != 0:
        res = False
        with open(f"logs/{solution.parent.stem}.log", "+a") as f:
            f.write("\n## Memory leak:\n")
            f.write(result.stderr.decode())

    return res


def main():
    parser = argparse.ArgumentParser(description="Check solutions")
    parser.add_argument(
        "-d", "--destination", help="Destination folder", default="logs"
    )
    parser.add_argument(
        "-s", "--source-folder", help="Source folder", default="solutions"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        help="Log level",
        default="INFO",
        choices=["INFO", "DEBUG", "ERROR", "WARNING"],
    )
    parser.add_argument(
        "-f",
        "--formatting",
        help="Check formatting",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r", "--runtime", help="Check runtime", action="store_true", default=True
    )
    parser.add_argument(
        "-v",
        "--valgrind",
        help="Check memory leak with valgrind",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    for solution in sorted(SOLUTIONS.glob("**/*.c")):
        if solution.suffix != ".c":
            continue

        content = solution.read_text()
        content = rules.delete_comments(content, to_=content.index("SEGUE!!!"))

        functions = rules.parse_functions(
            content,
            from_=content.index("#include <stdlib.h>"),
            to_=content.index("NON MODIFICARE"),
        )

        for name in ["uniformColor", "countColors"]:
            func = list(filter(lambda f: f.name == name, functions))[0]
            if not func.is_recursive():
                log.error(f"{solution.parent.stem} - {name} is not recursive")

        compiled = check_compilation(solution)
        if not compiled:
            log.error(f"Failed to compile {solution.parent.stem}")
            continue

        run = check_runtime(solution)
        match run:
            case 0:
                pass
            case 1:
                log.warning(f"{solution.parent.stem} did not pass all tests")
            case -1:
                log.error(f"Runtime error in {solution.parent.stem}")

        mem_leak_ok = check_valgrind(solution)
        if not mem_leak_ok:
            log.warning(f"Memory leak in {solution.parent.stem}")

        # formatting = check_formatting(solution)
        # if formatting:
        #     log.info(f"{solution} is well formatted")

        if compiled and run == 0 and mem_leak_ok:
            log.info(f"{solution.parent.stem} is OK")

        os.remove(FILE_NAME)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
