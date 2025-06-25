import subprocess
from utils import CompilationResult, CheckResult
import re


def check_invalid_rvalue(compilation_result: CompilationResult, config: dict) -> CheckResult:
    """
    Verifica se l'output di compilazione di GCC contiene un errore relativo a un r-value non valido.

    Un errore di r-value si verifica quando l'espressione a destra di un'assegnazione
    o in un contesto dove è atteso un valore, non è valida. L'esempio fornito
    dall'utente (`expected expression before ']' token`) è un caso perfetto.

    Args:
        compilation_text_out: Una stringa contenente l'output (stdout e stderr)
                              del processo di compilazione.

    Returns:
        True se viene trovato un errore di r-value, False altrimenti.
    """
    # Il pattern cerca la stringa "error:" seguita dalla frase "expected expression".
    # Questo copre il caso dell'utente e altri casi simili in cui il valore
    # a destra dell'assegnazione è sintatticamente scorretto.
    pattern = r"error:.*expected expression"
    if re.search(pattern, compilation_result.output):
        return CheckResult(
            error="Invalid r-value detected in the code. "
                  "This usually means that the right-hand side of an assignment is not a valid expression.",
            points=config["points"]["invalid_rvalue"]
        )
    return CheckResult()
