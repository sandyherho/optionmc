from setuptools import setup, find_packages

setup(
    name="optionmc",
    version="0.1.2",
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
    description="Monte Carlo Option Pricing with Educational Visualizations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sandyherho/optionmc",
    license="WTFPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
    ],
)
