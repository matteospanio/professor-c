#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
import subprocess
import sys
from rich.logging import RichHandler
import rules
from config import (
    FORMATTING,
    COMPILE_CMD,
    FILE_NAME,
    VALGRIND,
    MAX_POINTS,
    RECURSIVE_FUNCTIONS,
    Errors,
)

logging.basicConfig(
    format="%(message)s",
    datefmt="[%X]",
    level="NOTSET",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger(__name__)


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
    try:
        result = subprocess.run(f"./{FILE_NAME}", shell=True, capture_output=True, timeout=5)
        if result.returncode != 0:
            res = -1
            with open(f"logs/{solution.parent.stem}.log", "+a") as f:
                f.write("\n## Runtime error:\n")
                f.write(result.stderr.decode())
    except subprocess.TimeoutExpired:
        res = -1
        with open(f"logs/{solution.parent.stem}.log", "+a") as f:
            f.write("\n## Runtime error:\n")
            f.write("Timeout expired while running the program")

    # if "Tutti i test sono passati!" not in str(result.stdout):
    #     res = 1

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
        log.warning(f"{solution.parent.stem} warning shows up during compilation")

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
        "-v",
        "--valgrind",
        help="Check memory leak with valgrind",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    solutions = pathlib.Path(args.source_folder)
    destination = pathlib.Path(args.destination)
    valgrind = args.valgrind

    if not solutions.exists():
        log.critical(f"{solutions} does not exist")
        sys.exit(os.EX_NOINPUT)

    if not solutions.is_dir():
        log.critical(f"{solutions} is not a directory")
        sys.exit(os.EX_NOINPUT)

    if not solutions.glob("**/*.c"):
        log.critical(f"No C files found in {solutions}")
        sys.exit(os.EX_NOINPUT)

    if not destination.exists():
        destination.mkdir()

    if not destination.is_dir():
        log.critical(f"{destination} is not a directory")
        sys.exit(os.EX_NOINPUT)

    for log_file in destination.glob("*.log"):
        log_file.unlink()

    results: list[tuple[str, int]] = []

    for solution in sorted(solutions.glob("**/*.c")):
        points = MAX_POINTS

        if solution.suffix != ".c":
            continue

        content = solution.read_text()
        content = rules.delete_comments(content, to_=content.index("SEGUE!!!"))

        try:
            functions = rules.parse_functions(
                content,
                from_=content.index("#include <stdlib.h>"),
                to_=content.index("NON MODIFICARE"),
            )
        except IndexError as e:
            log.error(f"Failed to parse functions in {solution.parent.stem}: {e}")
            points -= Errors.UNBALANCED_BRACES
            results.append((" ".join(solution.parent.stem.split("_")[1:]), points))
            continue

        for name in RECURSIVE_FUNCTIONS:
            func = list(filter(lambda f: f.name == name, functions))[0]
            if not func.is_recursive():
                log.error(f"{solution.parent.stem} - {name} is not recursive")
                points -= Errors.NO_RECURSION

        compiles = check_compilation(solution)
        if not compiles:
            log.error(f"Failed to compile {solution.parent.stem}")
            points -= Errors.COMPILATION
            results.append((" ".join(solution.parent.stem.split("_")[1:]), points))
            continue

        run = check_runtime(solution)
        match run:
            case 0:
                pass
            case 1:
                log.warning(f"{solution.parent.stem} did not pass all tests")
                points -= Errors.RUNTIME
            case -1:
                log.error(f"Runtime error in {solution.parent.stem}")
                points -= 3

        if valgrind:
            mem_leak_ok = check_valgrind(solution)
            if not mem_leak_ok:
                log.warning(f"Memory leak in {solution.parent.stem}")
                points -= Errors.VALGRIND

        results.append((" ".join(solution.parent.stem.split("_")[1:]), points))
        if compiles and run == 0 and mem_leak_ok if valgrind else True:
            log.info(f"{solution.parent.stem} is OK")

        os.remove(FILE_NAME)

    for name, points in results:
        log.info(f"{name}: {points}")

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
