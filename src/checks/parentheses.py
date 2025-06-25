from utils import CheckResult
from pathlib import Path
import rules


def check_parentheses(solution: Path, config: dict) -> CheckResult:
        content = solution.read_text()
        content = rules.delete_comments(content, to_=content.index("SEGUE!!!"))

        try:
            rules.parse_functions(
                content,
                from_=content.index("#include <stdlib.h>"),
                to_=content.index("NON MODIFICARE"),
            )
        except IndexError as e:
            return CheckResult(
                error="Failed to parse functions, unmatched parenthesis likely",
                points=config["points"]["unmatched_parenthesis"]
            )

        return CheckResult()
