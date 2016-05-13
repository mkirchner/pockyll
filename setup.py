from setuptools import setup

from codecs import open
from os import path
with open(path.join(path.dirname(path.realpath(__file__)), 'README.md'), 
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "pockyll",
    description = "sync your pocket bookmarks to Jekyll linkposts",
    long_description = long_description,
    version = "0.1.1",
    author = 'Marc Kirchner',
    author_email = "mail@marc-kirchner.de",

    url = 'https://github.com/mkirchner/pockyll/',
    license = 'MIT',


classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords = 'jekyll pocket blog linkpost',
    install_requires = ["pocket", "PyYAML"],
    py_modules = ["pockyll"],
    entry_points={
        'console_scripts': [
            'pockyll=pockyll:main',
        ],
    },
)
