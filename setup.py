import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QuickAR",
    version="0.0.1",
    author="Ian Sodersjerna",
    author_email="Ian@sodersjerna.com",
    description="easy to implement AR-tag package for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plop91/QuickAR",
    project_urls={
        "Bug Tracker": "https://github.com/plop91/QuickAR/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)