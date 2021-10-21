import sys

from setuptools import setup

assert sys.version_info >= (3, 6), "fix-logseq-dates requires Python 3.6+"

from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))


def get_long_description() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


setup(
    name="fix-logseq-dates",
    version="2021.10.21",
    url="https://github.com/idadzie/fix-logseq-dates",
    license="MIT",
    author="Isaac Dadzie",
    author_email="hello@idadzie.dev",
    description="CLI tool to fix linked references for dates.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=[
        "arrow>=1.2.0",
        "dateparser>=1.1.0",
        "regex>=2021.10.8",
    ],
    py_modules=["fix_logseq_dates"],
    entry_points={"console_scripts": ["fix-logseq-dates=fix_logseq_dates:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
