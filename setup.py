import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dic_academic_parser",
    version='0.0.5',
    author="drforse",
    author_email="george.lifeslice@gmail.com",
    description="A package for parsing dic.academic.ru",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drforse/dic_academic_parser",
    install_requires=["requests==2.24.0", "beautifulsoup4==4.9.1", "lxml==4.5.2", "urlpath==1.1.7"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)