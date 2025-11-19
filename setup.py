#!/usr/bin/env python3
# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
#
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
MAYA Node Setup Script

This setup.py is provided for backward compatibility.
Modern installations should use pyproject.toml with pip install.

Installation:
    pip install -e .              # Development mode
    pip install -e ".[dev]"       # With development dependencies
    pip install -e ".[docs]"      # With documentation dependencies
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "MAYA Node - Sovereign AI infrastructure with ethical constraints"

setup(
    name="maya-node",
    version="0.5.0",
    description="Sovereign AI infrastructure with ethical constraints and transparent decision-making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MAYA Node Contributors",
    license="CERL-1.0",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.11",
    install_requires=[
        "flask>=3.0.0,<4.0.0",
        "flask-cors>=4.0.0,<5.0.0",
        "pytest>=7.4.0,<8.0.0",
        "pytest-cov>=4.1.0,<5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "pytest-asyncio>=0.21.0,<1.0.0",
            "coverage>=7.3.0,<8.0.0",
            "bandit>=1.7.5,<2.0.0",
            "safety>=2.3.0,<3.0.0",
            "pylint>=3.0.0,<4.0.0",
            "flake8>=6.1.0,<7.0.0",
            "black>=23.11.0,<24.0.0",
            "mypy>=1.7.0,<2.0.0",
            "isort>=5.12.0,<6.0.0",
            "pre-commit>=3.5.0,<4.0.0",
            "ipython>=8.17.0,<9.0.0",
            "ipdb>=0.13.13,<1.0.0",
        ],
        "docs": [
            "sphinx>=7.2.0,<8.0.0",
            "sphinx-rtd-theme>=2.0.0,<3.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ai ethics sovereign cerl distributed transparency",
)
