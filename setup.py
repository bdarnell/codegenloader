#!/usr/bin/env python

from distutils.core import setup

version = "0.1"

setup(
    name="codegenloader",
    version=version,
    packages=[
        "codegenloader",
        "codegenloader.test",
        "codegenloader.test.proto",
        ],
    package_data={
        "codegenloader.test.proto": ["simple.proto"],
        "codegenloader.test": ["thrift/simple.thrift"],
        },
    author="Ben Darnell",
    )
