
from setuptools import setup, find_packages
import sys, os

setup(name='VCLOpsworks',
    version='0.1',
    description="vcl opsworks",
    long_description="vcl opsworks",
    classifiers=[],
    keywords='',
    author='Akkaash Goel',
    author_email='agoel3@ncsu.edu',
    url='https://akkaash.github.io',
    license='BSD-3-Clause',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        ### Required to build documentation
        # "Sphinx >= 1.0",
        ### Required for testing
        # "nose",
        # "coverage",
        "click",
        "requests",
        "ansible"
        ],
    setup_requires=[],
    entry_points="""
        [console_scripts]
        vcl-opsworks=VCLOpsworks:cli
    """,
    namespace_packages=[],
    )
