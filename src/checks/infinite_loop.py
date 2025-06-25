from utils import CompilationResult, CheckResult
import subprocess

def check_infinite_loop(solution: CompilationResult, config: dict) -> CheckResult:
    if solution.success:
        try:
            subprocess.run(
                ["./main"],
                timeout=5,  # Set a timeout to detect infinite loops
                capture_output=True,
                shell=True,
            )
        except subprocess.TimeoutExpired:
            return CheckResult(
                error="Infinite loop detected",
                points=config["points"]["infinite_loop"]
            )

    return CheckResult()
