"""
Python net library
"""
from setuptools import find_packages, setup

setup(
    name='pynetlib',
    version='0.1.0',
    url='https://github.com/migibert/pynetlib',
    license='MIT',
    author='Mikael Gibert',
    author_email='mikael.gibert@gmail.com',
    description='Python net library',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
)
