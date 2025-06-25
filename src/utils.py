import subprocess
from dataclasses import dataclass

COMPILE_CMD = "gcc -Wall -std=c99 -pedantic -Wextra -lm -o main \"{}\""

@dataclass
class CompilationResult:
    success: bool
    output: str


@dataclass
class CheckResult:
    error: str|None = None
    points: int = 0


def compile(file_path: str):
    """Compile the C source file.
    Returns True if compilation is successful, False otherwise.
    """
    result = subprocess.run(COMPILE_CMD.format(file_path), shell=True, capture_output=True)
    out = result.stderr.decode() + result.stdout.decode()

    return CompilationResult(
        success=result.returncode == 0,
        output=out
    )
