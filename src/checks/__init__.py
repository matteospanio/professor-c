from pathlib import Path
from .parentheses import check_parentheses
from .unused_argument import check_unused_argument
from .undefined_variable import check_undefined_variable
from .invalid_lvalue import check_invalid_lvalue
from .invalid_rvalue import check_invalid_rvalue
from .invalid_assignment import check_invalid_assignment
from .recursion import check_recursive_functions
from .invalid_results import check_pseudo_code

from .compilation import check_compilation
from .infinite_loop import check_infinite_loop
from .m_leak import check_valgrind
from .warnings import check_warnings

from utils import compile, CheckResult
from pathlib import Path

def run_checks(file_path: str, config) -> list[CheckResult]:

    result_checks = [
        check_compilation,
        check_infinite_loop,
        check_valgrind,
        check_warnings,
        check_unused_argument,
        check_undefined_variable,
        check_invalid_lvalue,
        check_invalid_rvalue,
        check_invalid_assignment,
        check_pseudo_code,
    ]

    checks = [
        check_parentheses,
        check_recursive_functions,
    ]
    results = []

    compilation_result = compile(file_path)
    for chk in result_checks:
        results.append(chk(compilation_result, config))

    for chk in checks:
        results.append(chk(Path(file_path), config))

    Path("main").unlink(missing_ok=True)

    return results
