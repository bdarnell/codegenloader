from __future__ import with_statement
import os
import shutil
import subprocess
import tempfile
from codegenloader.base import CodeGenLoader


class ProtobufLoader(CodeGenLoader):
    def protoname(self, relname):
        assert relname.endswith("_pb2")
        relname = relname[:-len("_pb2")]
        return os.path.abspath(os.path.join(self.basedir, relname + '.proto'))

    def can_generate(self, relname):
        if relname.endswith("_pb2"):
            return os.path.exists(self.protoname(relname))
        else:
            return False

    def generate(self, relname):
        tempdir = tempfile.mkdtemp(prefix='codegenloader')
        try:
            protodir, protofile = os.path.split(self.protoname(relname))
            subprocess.check_call(
                ["protoc",
                 "--python_out=.",
                 "--proto_path=%s" % protodir,
                 self.protoname(relname)],
                cwd=tempdir)
            relpath = relname + ".py"
            with open(os.path.join(tempdir, relpath)) as f:
                self.store_contents(relpath, f.read())
        finally:
            shutil.rmtree(tempdir)


def make_path(modname, basedir):
    """Returns a object to be set as ``__path__``.

    This is the visible entry point to this module.  To use it,
    assign the result of this function to ``__path__``::

        import dropbox.codegenloader.protobuf
        __path__ = dropbox.codegenloader.protobuf.make_path(__name__, "proto")

    The first argument should always be ``__name__``; the second is a
    directory name that contains the ``.proto`` files. (relative to the
    file where `make_path` is called).
    """
    return ProtobufLoader.register(modname, basedir)
