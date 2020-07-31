# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='htbapi',
    version='0.1.0',

    description='Hack the Box API',
    long_description=long_description,

    url='https://github.com/zachhanson94/htb',

    author='Zach Hanson',
    author_email='zachhanson94@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='hackthebox',

    packages=find_packages(),

    install_requires=['requests'],
)
