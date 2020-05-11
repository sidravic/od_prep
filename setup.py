import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="od-prep-sidravic", # Replace with your own username
    version="0.0.1",
    author="sidravic",
    author_email="sid.ravichandran@gmail.com",
    description="Converts any dataset created by labelmg to be used by fastai's get_annotation method",
    long_description="See readme",
    long_description_content_type="text/markdown",
    url="https://github.com/sidravic/od_prep",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)