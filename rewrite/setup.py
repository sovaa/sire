from setuptools import setup, find_packages
import sys, os

version = '0.3.0'

setup(name='sire',
      version=version,
      description="Simple Reminder",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='lists',
      author='Oscar Eriksson',
      author_email='oscar.eriks@gmail.com',
      url='sire.eldslott.org',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
      ],
      entry_points={
          'console_scripts': [
              'sire = sire:entrypoint',
          ],
      }
      )
