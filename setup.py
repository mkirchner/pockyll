from setuptools import setup

setup(
    name = "pockyll",
    description = "sync your pocket bookmarks to Jekyll linkposts",

    # version
    # third part for minor release
    # second when api changes
    # first when it becomes stable someday
    version = "0.1.0",
    author = 'Marc Kirchner',
    author_email = "mail@marc-kirchner.de",

    url = 'https://github.com/mkirchner/pockyll/',
    license = 'MIT',

    # as a practice no need to hard code version unless you know program wont
    # work unless the specific versions are used
    install_requires = ["pocket", ],

    py_modules = ["pockyll", "PyYAML"],

    zip_safe = True,
)
