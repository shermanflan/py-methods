import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-methods",
    version="1.0.0",
    author="Ricardo Guzman",
    author_email="shermanflan@gmail.com",
    description="A starter flask app with db.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shermanflan/flask-methods",
    # This indicates which packages to install.
    packages=setuptools.find_packages(),
    # This specifies which dependencies to install.
    install_requires=[
        'flask', 'pyodbc', 'adal'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)