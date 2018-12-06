from setuptools import setup, find_packages
import sys
import os

version = '0.1.1'

setup(name='rulez',
      version=version,
      description="Simple business rules engine configurable using YAML/JSON",
      long_description="""\
""",
      # Get strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[],

      keywords='business-rules rules reg',
      author='Izhar Firdaus',
      author_email='izhar@abyres.net',
      url='http://github.com/abyres/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'reg',
          'dectate',
          'boolean.py',
          'jsonpath_ng',
          'sqlalchemy'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
