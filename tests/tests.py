#!/usr/bin/env python

import unittest

from subprocess import run
from shutil import copy
import os
from filecmp import cmp
from pathlib import Path

import errno

from PDFS import pdfs

# run with 'python -m PDFS.tests.tests'


test_folder = Path(__file__).resolve().parent
script = test_folder.parent.joinpath("pdfs.py")


def remove(filename):
	try:
		os.remove(filename)
	except OSError as e:
		if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
			raise  # re-raise exception if a different error occurred


class Join(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.ref = test_folder.joinpath("dog_joined_ref.pdf")
		self.pdf1 = test_folder.joinpath("dog.pdf")
		self.pdf2 = test_folder.joinpath("dog2.pdf")

	def tearDown(self):
		remove(self.output)

	def test_join(self):
		pdfs.join(self.output, (self.pdf1, self.pdf2))
		self.assertTrue(cmp(self.output, self.ref, shallow=False))

	def test_join_file_descriptors(self):
		with open(self.pdf1, "rb") as pdf1:
			pdfs.join(self.output, (pdf1, self.pdf2))
		self.assertTrue(cmp(self.output, self.ref, shallow=False))

	def test_join_PathLike(self):
		pdfs.join(self.output, (Path(self.pdf1), self.pdf2))
		self.assertTrue(cmp(self.output, self.ref, shallow=False))


class Rotate(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.ref90 = test_folder.joinpath("dog_rot_90_ref.pdf")
		self.ref180 = test_folder.joinpath("dog_rot_180_ref.pdf")
		self.ref270 = test_folder.joinpath("dog_rot_270_ref.pdf")
		self.pdf1 = test_folder.joinpath("dog.pdf")

		copy(self.pdf1, self.output)

	def tearDown(self):
		remove(self.output)

	def test_rotate_no_angle(self):
		pdfs.rotate(self.output, (0,), 90)
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	def test_rotate_90(self):
		pdfs.rotate(self.output, (0,), 90)
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	def test_rotate_180(self):
		pdfs.rotate(self.output, (0,), 180)
		self.assertTrue(cmp(self.output, self.ref180, shallow=False))

	def test_rotate_270(self):
		pdfs.rotate(self.output, (0,), 270)
		self.assertTrue(cmp(self.output, self.ref270, shallow=False))

	def test_rotate_page_string(self):
		pdfs.rotate(self.output, ("0",))
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	def test_rotate_match_types(self):
		pdfs.rotate(str(self.output), ["0"], 90)
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	@unittest.skip("output and pdf1 are not exactly the same and I need to"
	"develope a way to make sure the differences are minimal")
	def test_rotate_90_plus_270_equals_0(self):
		pdfs.rotate(self.output, ("0",))
		pdfs.rotate(self.output, ("0",), 270)
		self.assertTrue(cmp(self.output, self.pdf1, shallow=False))


class RotateTwoPages(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.pdf1 = test_folder.joinpath("dog_joined_ref.pdf")
		self.ref1_90 = test_folder.joinpath("dog_one_rot_90_ref.pdf")
		self.ref0_180 = test_folder.joinpath("dog_zero_rot_180_ref.pdf")
		self.ref01_270 = test_folder.joinpath("dog_both_rot_270_ref.pdf")

		copy(self.pdf1, self.output)

	def tearDown(self):
		remove(self.output)

	def test_rotate_one_of_two(self):
		pdfs.rotate(self.output, (1,))
		self.assertTrue(cmp(self.output, self.ref1_90, shallow=False))

	def test_rotate_other_one_of_two_180(self):
		pdfs.rotate(self.output, (0,), 180)
		self.assertTrue(cmp(self.output, self.ref0_180, shallow=False))

	def test_rotate_both_270(self):
		pdfs.rotate(self.output, (0, 1), 270)
		self.assertTrue(cmp(self.output, self.ref01_270, shallow=False))


class JoinScript(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.ref = test_folder.joinpath("dog_joined_ref.pdf")
		self.pdf1 = test_folder.joinpath("dog.pdf")
		self.pdf2 = test_folder.joinpath("dog2.pdf")

	def tearDown(self):
		remove(self.output)

	def test_join_pdfs(self):
		run([script, "join", self.output, self.pdf1, self.pdf2])
		self.assertTrue(cmp(self.output, self.ref, shallow=False))


class RotateScript(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_cpy.pdf")
		self.ref90 = test_folder.joinpath("dog_rot_90_ref.pdf")
		self.ref180 = test_folder.joinpath("dog_rot_180_ref.pdf")
		self.ref270 = test_folder.joinpath("dog_rot_270_ref.pdf")
		self.pdf1 = test_folder.joinpath("dog.pdf")

		copy(self.pdf1, self.output)

	def tearDown(self):
		remove(self.output)

	def test_rotate_no_angle(self):
		run([script, "rotate", self.output, "0"])
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	def test_rotate_90(self):
		run([script, "rotate", self.output, "0", "--90"])
		self.assertTrue(cmp(self.output, self.ref90, shallow=False))

	def test_rotate_180(self):
		run([script, "rotate", self.output, "0", "--180"])
		self.assertTrue(cmp(self.output, self.ref180, shallow=False))

	def test_rotate_270(self):
		run([script, "rotate", self.output, "0", "--270"])
		self.assertTrue(cmp(self.output, self.ref270, shallow=False))


class JoinJPGScript(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.ref = test_folder.joinpath("dog_jpg_joined_ref.pdf")
		self.jpg1 = test_folder.joinpath("dog.jpg")
		self.jpg2 = test_folder.joinpath("dog2.jpg")

	def tearDown(self):
		remove(self.output)

	def test_join_jpgs(self):
		run([script, "join", self.output, self.jpg1, self.jpg2])
		self.assertTrue(cmp(self.output, self.ref, shallow=False))


class JoinPNGScript(unittest.TestCase):
	def setUp(self):
		self.output = test_folder.joinpath("dog_output.pdf")
		self.ref = test_folder.joinpath("dog_jpg_joined_ref.pdf")
		self.png1 = test_folder.joinpath("dog.png")
		self.png2 = test_folder.joinpath("dog2.png")

	def tearDown(self):
		remove(self.output)

	@unittest.skip("dont have png files yet")
	def test_join_pngs(self):
		run([script, "join", self.output, self.png1, self.png2])
		self.assertTrue(cmp(self.output, self.ref, shallow=False))


if __name__ == "__main__":
	unittest.main()
