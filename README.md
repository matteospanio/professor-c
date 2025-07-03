# Correttore C

Correttore automatico per esercizi in C.

## How to use

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python src/main.py
   ```

## Configuration

You can configure the points penalty for each type of error in the `config.yaml` file. The default configuration is as follows:

```yaml
points:
  maximum: 11
  invalid_assignment: 2
  unmatched_parenthesis: 1
  recursion_required: 2
  infinite_loop: 2
  memory_leak: 1
  runtime_error: 1
  unused_argument: 1
  undefined_variable: 2
  invalid_lvalue: 1
  invalid_rvalue: 1
  compilation_error: 2
  execution_error: 2
  warnings: 0
  pseudo_code: 2

checks:
  unused_variables: true
  unused_functions: true
  unused_arguments: true
  undefined_variables: true
  invalid_lvalues: true
  invalid_rvalues: true
  compilation_errors: true
  execution_errors: true
  infinite_loops: true
  memory_leaks: true
  runtime_errors: true
  unmatched_parentheses: true
  recursion_required: true

recursive_functions:
  allowed_functions:
```
