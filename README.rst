CodeGenLoader
=============

CodeGenLoader is a Python import hook that transparently runs a code
generator at import time, allowing the use of generated code without
a separate compilation step.  The package includes an extensible base
class as well as implementations for the Protocol Buffer and
Thrift code generators.

Installation
------------

::

    pip install codegenloader

Prerequisites
-------------

CodeGenLoader runs on Python 2.5, 2.6, 2.7, pypy, and Jython.  The base
class does not have any external dependencies, but to use the Thrift or
Protocol Buffer subclasses you will need the thrift or protobuf packages
installed.

Example
-------

Add the following two lines to `mypackage/proto/__init__.py`::

    import codegenloader.protobuf
    __path__ = codegenloader.protobuf.make_path(__name__, ".")

Now, assuming `foo.proto` exists in in `mypackage/proto/`, you can do::

    from mypackage.proto.foo_pb2 import Foo

More info
---------

The source code is hosted at https://github.com/bdarnell/codegenloader
Detailed documentation can be found at http://codegenloader.readthedocs.org
