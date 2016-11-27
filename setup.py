import os
from setuptools import setup
from setuptools import find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "an_example_pypi_project",
    version = "1.0",
    author = "David Winer",
    author_email = "drwiner@cs.utah.edu",
    description = ("A Decompositional Word Visualization Tool"),
    license = "BSD",
    keywords = "Navon word visualization decomposition",
    url = "www.github.com/drwiner/pynavon",
	py_modules=['Board', 'Pattern'],
    packages=find_packages(),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)