from __future__ import with_statement
import glob
import os
import shutil
import subprocess
import tempfile
from codegenloader.base import CodeGenLoader


class ThriftLoader(CodeGenLoader):
    def thriftname(self, relname):
        return os.path.abspath(os.path.join(self.basedir, relname + '.thrift'))

    def can_generate(self, relname):
        return os.path.exists(self.thriftname(relname))

    def generate(self, relname):
        tempdir = tempfile.mkdtemp(prefix='codegenloader')
        try:
            subprocess.check_call(
                ["thrift", "--gen", "py:new_style", self.thriftname(relname)],
                cwd=tempdir)
            outdir = os.path.join(tempdir, 'gen-py')
            for fn in glob.glob("%s/%s/*.py" % (outdir, relname)):
                assert fn.startswith(outdir + '/')
                relpath = fn[len(outdir) + 1:]
                with open(fn) as f:
                    self.store_contents(relpath, f.read())
        finally:
            shutil.rmtree(tempdir)


def make_path(modname, basedir):
    """Returns a object to be set as ``__path__``.

    This is the visible entry point to this module.  To use it,
    assign the result of this function to ``__path__``::

        import dropbox.codegenloader.thrift
        __path__ = dropbox.codegenloader.thrift.make_path(__name__, "thrift")

    The first argument should always be ``__name__``; the second is a
    directory name that contains the thrift files. (relative to the
    file where `make_path` is called).
    """
    return ThriftLoader.register(modname, basedir)
