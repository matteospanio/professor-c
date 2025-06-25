from pathlib import Path
from checks import run_checks

def analyze_submissions(config, workdir: str):
    results = []
    for src in sorted(Path(workdir).glob("**/*.c")):
        student = src.parent.name.split("_")[0]
        check_results = run_checks(str(src), config)
        points = config["points"]["maximum"] - sum(result.points for result in check_results)
        errors = [result.error for result in check_results if result.error]
        results.append({
            "student": student,
            "points": points,
            "errors": errors,
        })
    return results
