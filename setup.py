"""
Setup script for dh5-api package.
This file provides backward compatibility for older pip versions.
Modern installations should use pyproject.toml.
"""

from setuptools import setup

# Read the contents of README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (
    (this_directory / "README.md").read_text(encoding="utf-8")
    if (this_directory / "README.md").exists()
    else ""
)

setup(
    name="dh5-api",
    version="1.0.0",
    description="Python API for Modbus communication with DH5 robot controllers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/dh5-api",
    packages=["dh5_api"],
    python_requires=">=3.8",
    install_requires=[
        "loguru>=0.7.0",
        "pymodbus>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    keywords="modbus dh5 robot controller automation",
    license="MIT",
)
