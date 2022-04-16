import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clean_folder",
    version="0.0.1",
    author="Max",
    author_email="max@example.com",
    description="Sorting files into folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxdetsyk/goit_python",
    project_urls={
        "Bug Tracker": "https://github.com/maxdetsyk/goit_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "clean_folder"},
    packages=setuptools.find_packages(where="clean_folder"),
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:cleaning']}
)

