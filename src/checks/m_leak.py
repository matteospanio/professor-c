import subprocess

from utils import CompilationResult, CheckResult

VALGRIND = "valgrind --leak-check=full --error-exitcode=1 ./main"

def check_valgrind(compilation_result: CompilationResult , config: dict) -> CheckResult:
    if compilation_result.success:
        try:
            result = subprocess.run(VALGRIND, shell=True, capture_output=True, timeout=5)
            if result.returncode != 0:
                return CheckResult(
                    error="Memory leak detected",
                    points=config["points"]["memory_leak"]
                )
        except subprocess.TimeoutExpired:
            pass
    return CheckResult()
