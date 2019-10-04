import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DAQdata",
    version="2.0",
    author="Sumeet Kumar Sinha",
    author_email="sumeet.kumar507@gmail.com",
    description="Read and plot slow and fast data binary files from centrifuge experiments conducted at Center of Geotechnical Modeling at University of California Davis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SumeetSinha/DAQdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Centrifuge Research at Center of Geotechnical Modeling at UC Davis",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
    
    keywords='Centrifuge, Center of Geotechnical MOdeling, CGM, UC Davis, Binary Data',

    install_requires=['matplotlib'],

    py_modules=["DAQdata"],
)


# python -m pip install --user --upgrade setuptools wheel

# python setup.py sdist bdist_wheel