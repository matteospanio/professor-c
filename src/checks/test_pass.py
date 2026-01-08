from utils import CompilationResult, CheckResult
import subprocess


def check_test_pass(solution: CompilationResult, config: dict) -> CheckResult:
    if solution.success:
        try:
            process = subprocess.run(
                ["./main"],
                timeout=5,  # Set a timeout to detect infinite loops
                capture_output=True,
                shell=True,
            )
        except subprocess.TimeoutExpired:
            return CheckResult(
                error="Infinite loop detected", points=config["points"]["infinite_loop"]
            )

        if "Qualcosa è andato storto" in process.stdout.decode():
            return CheckResult(
                error="The program did not pass the tests",
                points=config["points"]["test_failed"],
            )

    return CheckResult()
