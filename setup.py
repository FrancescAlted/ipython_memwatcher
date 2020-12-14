#!/usr/bin/env python
"""ipython_memwatcher: display memory usage during IPython execution

ipython_memwatcher is an IPython tool to report memory usage deltas for
every command you type.

This is strongly based on
https://github.com/ianozsvald/ipython_memory_usage by Ian Ozsvald and in
the future ipython_memwatcher can merged back into ipython_memory_usage.
"""

doclines = __doc__.split("\n")

# Chosen from http://www.python.org/pypi?:action=list_classifiers
classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
License :: Free To Use But Restricted
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
"""

from setuptools import setup, find_packages
setup(
    name="ipython_memwatcher",
    version="0.2.5",
    url="https://github.com/FrancescAlted/ipython_memwatcher",
    author="Francesc Alted, Ian Ozsvald",
    author_email="faltet@gmail.com",
    maintainer="Francesc Alted",
    maintainer_email="faltet@gmail.com",
    description=doclines[0],
    long_description="\n".join(doclines[2:]),
    classifiers=filter(None, classifiers.split("\n")),
    platforms=["Any."],
    packages=['ipython_memwatcher'],
    #package_dir={'ipython_memwatcher': 'ipython_memwatcher'},
    install_requires=['IPython>=3.1', 'memory_profiler'],
)
