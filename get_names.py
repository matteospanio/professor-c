import os
import pathlib as pl
import argparse as ap


def main():
    parser = ap.ArgumentParser(description="Check solutions")
    parser.add_argument("dir", type=pl.Path, help="Directory with solutions")
    args = parser.parse_args()

    d = pl.Path(args.dir)

    names = []

    for elem in d.iterdir():
        name = str(elem).split("/")[-1]
        parts = name.split("_")
        n = parts[0]
        x = parts[1]

        name = "_".join(n.split())
        folder_name = "_".join([x, name])
        names.append(folder_name)

        os.rename(elem, d / folder_name)


if __name__ == "__main__":
    main()
