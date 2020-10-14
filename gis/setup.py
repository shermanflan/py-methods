import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-gis-rrguzman1976",
    version="0.0.1",
    author="Ricardo Guzman",
    author_email="rrguzman1976@hotmail.com",
    description="A set of library modules for GIS tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rrguzman1976/python-gis",
    # This indicates which packages to install.
    packages=['python_gis'], # Or dynamically via: setuptools.find_packages(),
    # This specifies which dependencies to install.
    install_requires=[
        'shapely[vectorized]'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)