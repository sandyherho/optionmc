from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="optionmc",
    version="0.1.3.4",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "optionmc=optionmc.cli:main",
        ],
    },
    author="Sandy Herho",
    author_email="sandy.herho@email.ucr.edu",
    description="Monte Carlo simulation for European option pricing with visualization capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandyherho/optionmc",
    project_urls={
        "Documentation": "https://github.com/sandyherho/optionmc",
        "Bug Reports": "https://github.com/sandyherho/optionmc/issues",
        "Source Code": "https://github.com/sandyherho/optionmc",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="finance, options, monte carlo, black-scholes, simulation, derivatives, pricing",
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "optionmc": ["examples/*.py"],
    },
)
