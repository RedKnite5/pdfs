#!/usr/bin/env python

"""Usage:
	pdfs.py join <newfile> <files>...
	pdfs.py rotate <file> <pages>... [--180 --270]

Join jpgs, pngs, and pdfs into singular pdf files, then rotate individual
pages.
"""

from typing import IO
from collections.abc import Iterable, Container
from os import PathLike

from io import BytesIO

from docopt import docopt
import PyPDF2 as pdf  # type: ignore
import img2pdf        # type: ignore

PathType = str | bytes | PathLike[str] | PathLike[bytes] | int
Reader_and_open = str | PathLike[str] | PathLike[bytes]

__all__ = [
	"join",
	"rotate"
]


def _make_reader(file: str | IO | PathLike) -> pdf.PdfReader:
	if not hasattr(file, "read"):
		file = str(file)

	try:
		file = BytesIO(img2pdf.convert(file))
	except img2pdf.ImageOpenError:
		pass

	return pdf.PdfReader(file)


def join(newfile: PathType, files: Iterable[str | IO | PathLike]) -> None:
	"""Join pdf, jpg, and png files together into a single pdf

	newfile: the filename or file descriptor to write the output to

	files: an iterable containing the filenames or file descriptors of the
	files to be joined together"""

	writer = pdf.PdfWriter()
	readers = [_make_reader(fn) for fn in files]

	for reader in readers:
		for page in reader.pages:
			writer.add_page(page)

	with open(newfile, "wb") as file:
		writer.write(file)


def rotate(
	filename: Reader_and_open, pages: Container[int | str], angle: int = 90
) -> None:
	"""Rotate individual pages of a pdf

	filename: a string or a pathlike object representing the file to be modified

	pages: a container containing the page numbers to rotate

	angle: 90, 180, or 270, indicating how much to rotate the indicated pages
	by clockwise"""

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

def main():
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


if __name__ == "__main__":
	main()
