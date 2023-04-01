from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A utility to join pdf files together and rotate pages"
LONG_DESCRIPTION = """A utility to combine jpg, png, and pdf files together
into a single pdf file. """

setup(
       # the name must match the folder name
        name="PDFS", 
        version=VERSION,
        author="Max Friedman",
        author_email="<maxfriedman08@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["docopt", "PyPDF2", "img2pdf"],
		scripts=["PDFS/pdfs.py"],

        keywords=["python", "first package", "pdf"],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: End Users/Desktop",
			"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
			"Operating System :: POSIX :: Linux",
			"Topic :: Multimedia :: Graphics",
			"Typing :: Typed",
        ]
)
