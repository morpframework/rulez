import os
import sys

from setuptools import find_packages, setup

version = "0.1.4"

def readfile(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        out = f.read()
    return out

desc = '\n'.join([readfile('README.rst'), readfile('CHANGELOG.rst')])

setup(
    name="rulez",
    version=version,
    description="Simple business rules engine configurable using YAML/JSON",
    long_description=desc,
    # Get strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords="business-rules rules reg",
    author="Izhar Firdaus",
    author_email="izhar@abyres.net",
    url="http://github.com/abyres/",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "reg",
        "dectate",
        "boolean.py",
        "jsonpath_ng",
        "sqlalchemy"
        # -*- Extra requirements: -*-
    ],
    extras_require={
        "test": [
            "mirakuru",
            "elasticsearch>=5.0.0,<6.0.0",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      """,
)
