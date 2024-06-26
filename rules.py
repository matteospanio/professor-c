from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class Function:
    body: str
    name: str
    params: list[str]
    prototype: str
    return_type: str

    def __init__(self, body: str, name: str, params: list[str], return_type: str):
        self.body = body
        self.name = name
        self.params = params
        self.return_type = return_type

    @property
    def prototype(self) -> str:
        return f"{self.return_type} {self.name}({', '.join(self.params)})"

    def __str__(self):
        return f"{self.prototype} {self.body}"

    def is_recursive(self) -> bool:
        return self.name in self.body


def get_function_name(func: str) -> str:
    return func.split()[1].split("(")[0].strip("* \t\n")


def get_function_params(func: str) -> list[str]:
    params = func.split("(")[1].split(")")[0].split(",")
    return [param.strip("* \t\n") for param in params]


def get_return_type(func: str) -> str:
    return func.split()[0].strip("* \t\n")


@dataclass(frozen=True)
class Typedef:
    name: str
    type: str


@dataclass(frozen=True)
class _FuncBody:
    start_idx: int
    end_idx: int
    content: str


def delete_comments(txt: str, from_: int = 0, to_: int = -1) -> str:
    src = txt[from_:to_]

    stack = []
    matches = []

    for i, c in enumerate(src):
        if c == "/" and src[i + 1] == "*":
            stack.append(i)
        elif c == "*" and src[i + 1] == "/":
            start = stack.pop()
            if not stack:
                matches.append((start, i + 1))

    res = ""
    last_end = 0
    for start, end in matches:
        res += src[last_end:start]
        last_end = end + 1

    res += src[last_end:]

    lines = []
    for line in res.splitlines():
        try:
            cmt_idx = line.index("//")
            lines.append(line[:cmt_idx])
        except ValueError:
            lines.append(line)

    return "\n".join(filter(lambda s: s != "", "\n".join(lines).splitlines()))


def parse_functions(txt: str, from_: int = 0, to_: int | None = None) -> list[Function]:
    if to_ is None:
        src = txt[from_:]
    else:
        src = txt[from_:to_]

    stack = []
    matches: list[_FuncBody] = []
    functions: list[Function] = []

    for i, c in enumerate(src):
        if c == "{":
            stack.append(i)
        elif c == "}":
            start = stack.pop()
            if not stack:
                matches.append(_FuncBody(start, i, src[start : i + 1]))

    if stack:
        logger.error("Unbalanced braces")

    for m in matches:
        try:
            name = max(src.rindex(";", 0, m.start_idx), src.rindex("}", 0, m.start_idx))
        except ValueError:
            name = 0

        before_func = "\n".join(
            filter(
                lambda s: s != "" and not s.startswith("#"),
                (src[name : m.start_idx]
                    .strip(" \t\n;}")
                    .splitlines()
                )
            )
        )

        if not (before_func.startswith("typedef") or before_func.startswith("static")):
            name = get_function_name(before_func)
            params = get_function_params(before_func)
            return_type = get_return_type(before_func)

            foo = Function(m.content, name, params, return_type)
            functions.append(foo)

    return functions


if __name__ == "__main__":
    CPROG = """
#include <stdio.h>

/*
 * commento
 */

typedef struct {
    int x; // commento
    int y; /* aaa */

    /*bbb*/
} Point;

int distance(Point *p1, Point *p2) {
    return (p1->x - p2->x) * (p1->x - p2->x) + (p1->y - p2->y) * (p1->y - p2->y);
}

int main(void) {
    printf("Hello, world!\\n");
    return 0;
}
"""
    src = delete_comments(CPROG)

    functions = parse_functions(src)
    for func in functions:
        print(func.prototype)
