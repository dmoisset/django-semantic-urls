import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django_semantic_urls",
    version = "0.1",
    author = "Daniel F Moisset",
    author_email = "dmoisset@machinalis.com",
    description = ("Define Django URL patterns with a semantics-oriented, clean syntax"),
    license = "BSD",
    keywords = "django urls",
    url = "http://github.com/dmoisset/django-semantic-urls/",
    packages=['semantic_urls', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)


