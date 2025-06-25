from utils import CompilationResult, CheckResult

def check_compilation(compilation_result: CompilationResult, config: dict) -> CheckResult:
    """
    Check if the compilation was successful.
    """
    if not compilation_result.success:
        return CheckResult(
            "Compilation failed",
            config["points"]["compilation_error"]
        )

    return CheckResult()
