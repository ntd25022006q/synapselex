#!/usr/bin/env python3
"""
SynapseLex Setup Configuration
==============================
Packaging according to NeurIPS / ACM Open Science reproducibility standards.
"""

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

readme_path = os.path.join(here, "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="synapselex",
    version="0.1.0",
    author="Nguyen Tien Dat",
    author_email="ntd25022006q@gmail.com",
    maintainer="Nguyen Tien Dat (VNU-IS)",
    maintainer_email="ntd25022006q@gmail.com",
    description="SynapseLex: An Axiomatic Temporal State-Transition Graph Framework for Non-Monotonic Civil Legal Adjudication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datbazuka2502/synapselex",
    project_urls={
        "Affiliation": "International School, Vietnam National University, Hanoi (VNU-IS), Hanoi, Vietnam",
        "Repository": "https://github.com/datbazuka2502/synapselex",
    },
    package_dir={"synapselex": "."},
    packages=[
        "synapselex",
        "synapselex.src",
        "synapselex.src.models",
        "synapselex.src.data",
        "synapselex.src.extraction",
    ],
    py_modules=["cli"],
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "rdflib>=7.0.0",
        "networkx>=3.0",
        "scipy>=1.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": [
            "synapselex-predict = synapselex.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Legal Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)
