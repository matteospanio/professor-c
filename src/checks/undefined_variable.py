from utils import CompilationResult, CheckResult

def check_undefined_variable(compilation_result: CompilationResult, config: dict) -> CheckResult:
    if "error: ‘" in compilation_result.output and "undeclared" in compilation_result.output:
        return CheckResult(
            error="Undefined variable detected",
            points=config["points"]["undefined_variable"]
        )

    return CheckResult()
