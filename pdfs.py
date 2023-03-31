#!/usr/bin/env python

"""Usage:
	pdfs.py join <newfile> <files>...
	pdfs.py rotate [--180 --270] <file> <pages>..."""

from docopt import docopt
import PyPDF2 as pdf

from typing import IO
from collections.abc import Iterable
from os import PathLike

Path = str | bytes | PathLike[str] | PathLike[bytes] | int
Reader_and_open = str | PathLike[str] | PathLike[bytes]

__all__ = [
	"join",
	"rotate"
]

def join(newfile: Path, files: Iterable[str | IO | PathLike]) -> None:
	""" """

	writer = pdf.PdfWriter()
	readers = [pdf.PdfReader(fn) for fn in files]

	for reader in readers:
		for page in reader.pages:
			writer.add_page(page)

	with open(newfile, "wb") as file:
		writer.write(file)

def rotate(filename: Reader_and_open, pages: Iterable[int | str], angle: int=90) -> None:
	""" """

	writer = pdf.PdfWriter()
	reader = pdf.PdfReader(filename)

	for num, page in enumerate(reader.pages):
		if str(num) in pages or num in pages:
			page.rotate(angle)
		writer.add_page(page)

	with open(filename, "wb") as file:
		writer.write(file)


doc = """Usage:
	pdfs.py join <newfile> <files>...
	pdfs.py rotate <file> <pages>... [--90 --180 --270]
"""

if __name__ == "__main__":
	args = docopt(doc)

	if args["join"]:
		join(args["<newfile>"], args["<files>"])
	elif args["rotate"]:
		angle = 90
		if args["--180"]:
			angle = 180
		if args["--270"]:
			angle = 270
		rotate(args["<file>"], args["<pages>"], angle)
