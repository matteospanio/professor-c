import os
import pathlib as pl
import argparse as ap

from rich.console import Console


def main():
    parser = ap.ArgumentParser(description="Check solutions")
    parser.add_argument("dir", type=pl.Path, help="Directory with solutions")
    args = parser.parse_args()

    d = pl.Path(args.dir)
    console = Console()

    names = []

    for elem in d.iterdir():
        if not elem.is_dir():
            continue

        name = str(elem).split("/")[-1]
        parts = name.split("_")
        try:
            n = parts[0]
            x = parts[1]
        except IndexError:
            console.print("Error with file: ", elem)
            console.print_exception(show_locals=True)
            exit(os.EX_DATAERR)

        name = "_".join(n.split())
        folder_name = "_".join([x, name])
        names.append(folder_name)

        os.rename(elem, d / folder_name)


if __name__ == "__main__":
    main()
