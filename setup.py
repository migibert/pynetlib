"""
Python net library
"""
from setuptools import find_packages, setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
dependencies = [str(ir.req) for ir in install_reqs]

setup(
    name='pynetlib',
    version='0.3.0',
    url='https://github.com/migibert/pynetlib',
    license='MIT',
    author='Mikael Gibert',
    author_email='mikael.gibert@gmail.com',
    description='Python net library',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies,
)
