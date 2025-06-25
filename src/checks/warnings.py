from utils import CompilationResult, CheckResult

def check_warnings(compilation_result: CompilationResult, config: dict) -> CheckResult:
    if "warning" in compilation_result.output:
        return CheckResult(
            error="Warnings detected during compilation",
            points=config["points"]["warnings"]
        )

    return CheckResult()
