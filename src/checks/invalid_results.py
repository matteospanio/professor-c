from utils import CompilationResult, CheckResult
import subprocess
import re

def check_pseudo_code(solution: CompilationResult, config: dict) -> CheckResult:
    if solution.success:
        try:
            result = subprocess.run(
                ["./main"],
                timeout=3,  # Set a timeout to detect infinite loops
                capture_output=True,
                shell=True,
            )

            output = result.stdout.decode()
            error = result.stderr.decode()

            total_output = output + error

            if "Attenzione: ci sono ancora ordini in coda" in total_output:
                return CheckResult(
                    error="Unempty queue detected. The program did not process all orders.",
                    points=config["points"]["pseudo_code"]
                )

            # check if output contains negative numbers
            if re.search(r"\b-\d+\b", total_output):
                return CheckResult(
                    error="Negative numbers detected in output. The program should not produce negative values.",
                    points=config["points"]["pseudo_code"]
                )

        except subprocess.TimeoutExpired:
            return CheckResult()

    return CheckResult()
