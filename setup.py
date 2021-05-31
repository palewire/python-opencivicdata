#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'Django>=3.2.*',
    'psycopg2',
]

extras_require = {
    "dev": ["pytest>=3.6", "pytest-cov", "pytest-django", "coveralls", "flake8"]
}

setup(
    name="ccdc-opencivicdata",
    version="0.0.1",
    author="Ben Welsh",
    author_email="b@palewi.re",
    license="BSD",
    description="campaign finance fork for python opencivicdata library",
    long_description="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    platforms=["any"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
