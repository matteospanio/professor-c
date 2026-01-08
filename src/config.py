import yaml
from dataclasses import dataclass


def load_config(filename: str):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


@dataclass
class Points:
    maximum: int
    invalid_assignment: int
    unmatched_parenthesis: int
    recursion_required: int
    infinite_loop: int
    memory_leak: int
    runtime_error: int
    unused_argument: int
    undefuned_variable: int
    invalid_lvalue: int
    invalid_rvalue: int
    compilation_error: int
    warnings: int
    pseudo_code: int
    test_failed: int


@dataclass
class RecursiveFunctions:
    allowed_functions: list[str]


@dataclass
class Checks:
    unused_variables: bool
    unused_arguments: bool
    undefined_variables: bool
    invalid_lvalues: bool
    invalid_rvalues: bool
    compilation_errors: bool
    warnings: bool
    pseudo_code: bool
    recursion_required: bool
    test_pass: bool


@dataclass
class Config:
    points: Points
    recursive_functions: RecursiveFunctions
    checks: Checks

    @staticmethod
    def from_file(filename: str):
        config_data = load_config(filename)
        return Config(
            points=Points(**config_data["points"]),
            recursive_functions=RecursiveFunctions(
                **config_data["recursive_functions"]
            ),
            checks=Checks(**config_data["checks"]),
        )
