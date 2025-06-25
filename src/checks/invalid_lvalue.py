import subprocess
from utils import CompilationResult, CheckResult

def check_invalid_lvalue(comp_result: CompilationResult, config: dict) -> CheckResult:
    if "lvalue required" in comp_result.output:
        return CheckResult(
            error="Invalid lvalue detected",
            points=config["points"]["invalid_lvalue"]
        )
    return CheckResult(error=None, points=0)
