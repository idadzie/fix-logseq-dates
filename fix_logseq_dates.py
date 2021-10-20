import argparse
import fileinput
import shutil
import sys
from pathlib import Path

import dateparser
import regex


def sanitize_match(string):
    return regex.sub(r"(\[\[|title[:]{,2}\s|\]\])", "", string.strip())


def replace_line(line_, date_format="%B %d, %Y", any_date=False):
    pattern = (
        r"((?:\[\[|title[:]{,2}\s)?(?:\d{,2}\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
        r"Sep|Oct|Nov|Dec)[a-z]*(?:-|\.|\s|,)\s?\d{,2}[a-z]*(?:-|,|\s)?\s?\d{2,4}?"
        r"(?:\]\]|\s))"
    )
    if any_date:
        pattern = (
            r"((?:\d{,2}\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
            r"Sep|Oct|Nov|Dec)[a-z]*(?:-|\.|\s|,)\s?\d{,2}[a-z]*(?:-|,|\s)?\s?\d{2,4})"
        )

    try:
        match = sanitize_match(regex.findall(pattern, line_)[0])
    except (IndexError, AttributeError):
        return line_

    date_ = dateparser.parse(match)
    date_string = date_.strftime(date_format)
    return line_.replace(match, date_string)


def modify_file(path, date_format, any_date):
    with fileinput.FileInput(f"{path.absolute()}", inplace=True, backup=".bak") as f:
        for line in f:
            print(replace_line(line, date_format), end="")


def cleanup(path):
    backup = Path(f"{path.absolute()}.bak")
    backup.absolute().unlink()


def restore_file(path):
    possibly_broken = path.absolute()  # because FileInput...
    backup = Path(f"{path.absolute()}.bak").absolute()
    shutil.move(backup, possibly_broken)


def init_argparse():
    # TODO: Use Typer. ;D Moar dependencies. ¯\_(ツ)_/¯ Easier life?
    formatter = lambda prog: argparse.ArgumentDefaultsHelpFormatter(
        prog, max_help_position=52
    )
    parser = argparse.ArgumentParser(
        description="CLI tool to fix linked references for Logseq dates.",
        formatter_class=formatter,
    )
    parser.add_argument(
        "-f",
        type=str,
        default="%B %d, %Y",
        dest="format",
        help="date format.",
    )
    parser.add_argument(
        "-j",
        type=str,
        default="journals",
        dest="journals_directory",
        help="journals folder name.",
    )
    parser.add_argument(
        "-p",
        type=str,
        default="pages",
        dest="pages_directory",
        help="pages folder name.",
    )
    parser.add_argument(
        "-d",
        type=str,
        default=None,
        dest="graph_directory",
        help="absolute path to your local Logseq graph.",
    )
    parser.add_argument(
        "--any-date",
        action="store_true",
        help="match any date found not only referenced ones.",
    )
    return parser


def main():

    parser = init_argparse()
    args = parser.parse_args()

    logseq_directory = args.graph_directory
    if not logseq_directory:
        sys.exit(
            "Kindly provide the absolute path to your "
            "local copy of your logseq graph using."
        )

    date_format = args.format
    logseq_path = Path(logseq_directory).resolve()

    if not logseq_path.is_dir():
        sys.exit("Kindly provide a valid logseq directory.")

    any_date = args.any_date

    for path in logseq_path.iterdir():
        if path.name not in (args.journals_directory, args.pages_directory):
            continue

        for path_ in path.iterdir():
            if path_.is_file() and path_.suffix != ".bak":
                try:
                    modify_file(path_, date_format, any_date)
                    cleanup(path_)
                    # Broad! yes; don't @ me.
                except Exception:  # noqa
                    restore_file(path_)
    print("Done :D")


if __name__ == "__main__":
    main()
