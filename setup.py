import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-flask-data-structure",
    version="0.0.1",
    author="Mahfuz Ali",
    author_email="mahfuzali@hotmail.co.uk",
    description="Python flask data strucutre package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahfuzali/python-data-structure",
    project_urls={
        "Bug Tracker": "https://github.com/mahfuzali/python-data-structure/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)