from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="wrap-genius",
    version="1.5.1",
    url="https://github.com/fedecalendino/wrap-genius",
    license="MIT",
    description="Python wrapper for api.genius.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fede Calendino",
    author_email="fede@calendino.com",
    packages=["genius", "genius.classes"],
    install_requires=["unidecode"],
    keywords=[
        "python",
        "api",
        "genius",
        "lyrics",
        "genius-api",
        "genius-lyrics",
        "wrapper-api",
        "wrapper",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
