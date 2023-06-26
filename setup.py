#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = []

setup(
    author="Joe S",
    author_email="kenwood364@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    description="Virtual mouse lets you simulate your maze solving algorithms",
    # entry_points={
    #     "console_scripts": [
    #         "virtual_mouse=virtual_mouse.cli:main",
    #     ],
    # },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="virtual_mouse",
    name="virtual_mouse",
    packages=find_packages(include=["virtual_mouse", "virtual_mouse.*"]),
    tests_require=test_requirements,
    url="https://github.com/SNHU-Robotics/virtual_mouse",
    version="0.1.0",
    zip_safe=False,
)
