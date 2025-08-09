from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.3'
DESCRIPTION = 'Python client for Aira Home, initially developed for Homeassistant'

# Setting up
setup(
    name="pyairahome",
    version=VERSION,
    author="Invy55 (Marco)",
    author_email="<marco@invy55.win>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Invy55/pyairahome",
    packages=find_packages(),
    install_requires=['pycognito>=2024.5.1', 'grpcio>=1.72.0'],
    keywords=['python', 'aira', 'airahome', 'aira home', 'api', 'wrapper'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)