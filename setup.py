import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pleiades.datasets",
    version="2.0",
    author="Tom Elliott",
    author_email="tom.elliott@nyu.edu",
    description="Platform-independent data from the Pleiades gazetteer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pleiades.stoa.org",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "airtight",
        "beautifulsoup4",
        "cffconvert",
        "encoded_csv",
        "haversine",
        "lxml",
        "python-dateutil",
        "requests",
        "requests-cache",
        "shapely",
        "textnorm",
    ],
    python_requires=">=3.8.3",
)
