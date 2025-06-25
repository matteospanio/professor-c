import subprocess
from utils import CheckResult, CompilationResult

def check_unused_argument(com_res: CompilationResult, config: dict) -> CheckResult:
    if "-Wunused-but-set-parameter" in com_res.output:
        return CheckResult(
            error="Unused function argument detected",
            points=config["points"]["unused_argument"]
        )

    return CheckResult()
