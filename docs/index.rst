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

CodeGenLoader runs on Python 2 (2.5+) and 3, including pypy and
jython.  The base class does not have any external dependencies, but
to use the Thrift or Protocol Buffer subclasses you will need the
thrift or protobuf packages installed. Note that protobuf 3.0.0
(currently in alpha) is required to use protobuf on Python 3.

.. versionchanged:: 0.2
   Added Python 3 support.

Example
-------

Add the following two lines to `mypackage/proto/__init__.py`::

    import codegenloader.protobuf
    __path__ = codegenloader.protobuf.make_path(__name__, ".")

Now, assuming `foo.proto` exists in in `mypackage/proto/`, you can do::

    from mypackage.proto.foo_pb2 import Foo

Detailed docs
-------------

.. toctree::

   base
   protobuf
   thrift

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
