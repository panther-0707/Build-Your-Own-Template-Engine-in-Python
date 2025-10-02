"""Setup script for the Templite template engine."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="templite-engine",
    version="1.0.0",
    author="Based on Ned Batchelder's implementation",
    author_email="",
    description="A simple, fast template engine implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panther-0707/Build-Your-Own-Template-Engine-in-Python",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="template, templating, html, text-generation",
    project_urls={
        "Documentation": "https://github.com/panther-0707/Build-Your-Own-Template-Engine-in-Python/blob/main/README.md",
        "Source": "https://github.com/panther-0707/Build-Your-Own-Template-Engine-in-Python",
        "Tracker": "https://github.com/panther-0707/Build-Your-Own-Template-Engine-in-Python/issues",
    },
)
