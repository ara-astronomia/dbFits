import os
from setuptools import setup

# Development Status :: 1 - Planning
# Development Status :: 2 - Pre-Alpha
# Development Status :: 3 - Alpha
# Development Status :: 4 - Beta
# Development Status :: 5 - Production/Stable
# Development Status :: 6 - Mature
# Development Status :: 7 - Inactive
# Environment :: Console
# Environment :: Console :: Curses
# Environment :: Console :: Framebuffer
# Environment :: Console :: Newt
# Environment :: Console :: svgalib
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dbFit",
    version = "0.0.2",
    author = "Alessio Caradossi",
    author_email = "alkcxy@gmail.com",
    description = ("Walk a folder and his subtrees and parse the fits it founds to extrapolate the header and save it to a sqlite3 db or a csv file"),
    license = "BSD",
    keywords = "for csv, just execute fits.py -i <inputdir> -o <outputfile>",
    url = "not yet",
    install_requies=['pyfits,pythoncard'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE v3",
    ],
)
