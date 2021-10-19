import argparse
import fileinput
import shutil
import sys
from pathlib import Path

import dateparser
import regex


def replace_line(line_, date_format="%B %d, %Y"):
    rgx = (
        r"((?:\d{,2}\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
        r"Sep|Oct|Nov|Dec)[a-z]*(?:-|\.|\s|,)\s?\d{,2}[a-z]*(?:-|,|\s)?\s?\d{2,4})"
    )

    try:
        match = regex.findall(rgx, line_)[0]
    except IndexError:
        return line_

    date_ = dateparser.parse(match)
    date_string = date_.strftime(date_format)
    return line_.replace(match, date_string)


def modify_file(path, date_format):
    with fileinput.FileInput(f"{path.absolute()}", inplace=True, backup=".bak") as f:
        for line in f:
            print(replace_line(line, date_format), end="")


def cleanup(path):
    backup = Path(f"{path.absolute()}.bak")
    backup.absolute().unlink()


def restore_file(path):
    possibly_broken = path.absolute()  # because FileInput...
    backup = Path(f"{path.absolute()}.bak")
    shutil.move(backup.absolute(), possibly_broken)


def init_argparse():
    # TODO: Use Typer. ;D Moar dependencies. ¯\_(ツ)_/¯ Easier life?
    parser = argparse.ArgumentParser(
        description="CLI tool to fix linked references for Logseq dates."
    )
    parser.add_argument(
        "-f",
        type=str,
        default="%B %d, %Y",
        dest="format",
        help="date format.",
    )
    parser.add_argument(
        "-d",
        type=str,
        default=None,
        dest="directory",
        help="absolute path to your local copy of your logseq graph.",
    )
    return parser


def main():

    parser = init_argparse()
    args = parser.parse_args()

    logseq_directory = args.directory
    if not logseq_directory:
        sys.exit(
            "Kindly provide the absolute path to your "
            "local copy of your logseq graph using."
        )

    date_format = args.format
    logseq_path = Path(logseq_directory).resolve()

    if not logseq_path.is_dir():
        sys.exit("Kindly provide a valid logseq directory.")

    for path in logseq_path.iterdir():
        # TODO: What if not called journals & pages?
        #      Should cater for this.
        if path.name not in ("journals", "pages"):
            continue

        for path_ in path.iterdir():
            if path_.is_file() and path_.suffix != ".bak":
                try:
                    modify_file(path_, date_format)
                    cleanup(path_)
                    # Broad! yes; don't @ me.
                except Exception:  # noqa
                    restore_file(path_)
    print("Done :D")


if __name__ == "__main__":
    main()
