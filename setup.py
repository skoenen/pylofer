import os

from setuptools import setup

def read_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyprol",
    version="0.1.0",
    description="Python Performance Measure System",
    long_description=read_readme("README.md"),
    author="Stefan Koenen",
    author_email="stefan.koenen@uni-duesseldorf.de",
    url="https://github.com/skoenen/pyprol",
    packages=['pyprol',
              'pyprol.instrumentations',
              'pyprol.measurement',
              'pyprol.storage',
              'pyprol.utils'],
    entry_points={'paste.filter_factory': ['main=pyprol:inject']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Server',
        'Intended Audience :: Developer',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Profiling'
        ],
    install_requires=[
        'setuptools']
    )
