from os.path import abspath, dirname, join
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()

setup(
    name="tornado_circus",
    version="0.0.1",
    description="A tornado application compatible with circus socket",
    long_description=read_relative_file('README.rst'),
    author="Boris FELD",
    author_email="lothiraldan@gmail.com",
    license="BSD",
    url='https://github.com/Lothiraldan/tornado_circus',
    packages=['tornado_circus'],
    install_requires=[
        'tornado',
    ],
)
