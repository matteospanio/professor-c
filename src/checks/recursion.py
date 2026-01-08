import rules
from utils import CheckResult
from pathlib import Path


def check_recursive_functions(solution: Path, config: dict) -> CheckResult:
    content = solution.read_text()
    content = rules.delete_comments(content, to_=content.index("SEGUE!!!"))

    try:
        functions = rules.parse_functions(
            content,
            from_=content.index("#include <stdlib.h>"),
            to_=content.index("NON MODIFICARE"),
        )
    except IndexError as e:
        return CheckResult(
            error="Could not parse functions, hand check the code structure",
            points=config["points"]["warnings"],
        )

    if config["recursive_functions"]["allowed_functions"]:
        for name in config["recursive_functions"]["allowed_functions"]:
            func = list(filter(lambda f: f.name == name, functions))[0]
            if not func.is_recursive():
                return CheckResult(
                    error=f"Function '{name}' is not recursive",
                    points=config["points"]["recursion_required"],
                )

    return CheckResult()
