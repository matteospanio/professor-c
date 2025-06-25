from utils import CompilationResult, CheckResult

def check_invalid_assignment(comp_result: CompilationResult, config: dict) -> CheckResult:
    if "<-" in comp_result.output:
        return CheckResult(
            error="Invalid assignment operator '<-' used",
            points=config["points"]["invalid_assignment"]
        )
    return CheckResult(error=None, points=0)
