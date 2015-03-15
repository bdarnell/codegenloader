import imp
import itertools
import os
import sys

_counter = itertools.count()


if sys.version_info > (3,):
    exec("""
def exec_in(code, glob, loc=None):
    if isinstance(code, str):
        code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, glob, loc)
""")
else:
    exec("""
def exec_in(code, glob, loc=None):
    if isinstance(code, basestring):
        # exec(string) inherits the caller's future imports; compile
        # the string first to prevent that.
        code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec code in glob, loc
""")


class CodeGenLoader(object):
    """Abstract base class for code generation import hooks.

    The entry point for applications is to define a subclass
    and use the `register` class method to set __path__.
    This will make the module where __path__ was assigned
    a pseudo-package from which the generated code can be imported.

    The interface between this class and the python interpreter
    is defined in PEP 302:
    http://www.python.org/dev/peps/pep-0302/
    """
    # Class entry points
    @classmethod
    def register(cls, *args, **kwargs):
        """Registers an import hook.

        Arguments are passed (eventually) to `initialize`.
        """
        cls._install_hook()
        hook_key = '__codegenloader_%d' % next(_counter)
        if not hasattr(cls, "_register_args"):
            cls._register_args = {}
        cls._register_args[hook_key] = (args, kwargs)
        return [hook_key]

    @classmethod
    def _install_hook(cls):
        """Installs this loader as a ``path_hook``."""
        if hasattr(cls, "_hook_installed"):
            return
        sys.path_hooks.append(cls)
        cls._hook_installed = True

    # PEP302 implementation
    def __init__(self, path):
        """Constructs a CodeGenLoader.

        Implements the hook protocol from PEP 302: it is called with a
        "path", and returns a loader if we can handle that path
        (i.e. if the path is actually a unique token we created in
        `register`), or raises an ImportError if not.
        """
        if path in self._register_args:
            self.hook_key = path
            args, kwargs = self._register_args[path]
            self.initialize(*args, **kwargs)
        else:
            raise ImportError("not my path")

    def initialize(self, modname, basedir):
        """Real initialization function, independent of PEP302 requirements.

        ``modname`` is the module name relative to which the generated code
        will be imported.
        ``basedir`` is the directory in which the source files for generation
        can be found.  If it is not an absolute path, it is interpreted
        as relative to the file containing ``modname``
        """
        self.basename = modname + '.'
        if os.path.isabs(basedir):
            self.basedir = basedir
        else:
            self.basedir = os.path.join(
                os.path.dirname(sys.modules[modname].__file__), basedir)
        self.contents = {}

    def find_module(self, fullname):
        """Returns a loader object for the module ``fullname``, if it exists.

        Implements the "finder" portion of the PEP 302 interface.
        """
        relname = self.get_relname(fullname)
        try:
            self.get_contents(relname)
            # No error: we can load the module
            return self
        except KeyError:
            if not self.can_generate(relname):
                return None
            self.generate(relname)
            # Try again after generating
            try:
                self.get_contents(relname)
                return self
            except KeyError:
                # Still not there
                return None

    def load_module(self, fullname):
        """Returns the module named ``fullname``.

        Implements the "loader" portion of the PEP 302 interface.
        """
        relname = self.get_relname(fullname)
        # This should never fail since python always calls find_module first
        is_pkg, contents = self.get_contents(relname)
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = '<codegenloader %s>' % fullname
        mod.__loader__ = self
        if is_pkg:
            mod.__path__ = [self.hook_key]
        exec_in(contents, mod.__dict__)
        return mod

    # Internal methods
    def get_relname(self, fullname):
        """Converts a fully-qualified module name to a relative one."""
        assert fullname.startswith(self.basename)
        return fullname[len(self.basename):]

    def get_contents(self, relname):
        """Return a tuple (is_pkg, contents) if code is stored for this module.

        If the code is not found, raises KeyError.
        """
        relpath = relname.replace('.', '/')
        init_path = relpath + '/__init__.py'
        if init_path in self.contents:
            return True, self.contents[init_path]
        mod_path = relpath + '.py'
        if mod_path in self.contents:
            return False, self.contents[mod_path]
        raise KeyError("code not found for %s" % relname)

    def store_contents(self, relpath, contents):
        """Store the contents of a file at relpath.

        To be called from subclasses after code has been generated.
        """
        assert relpath not in self.contents
        self.contents[relpath] = contents

    # Methods for overriding in subclass
    def can_generate(self, relname):
        """Should return True if we can generate a module named ``relname``."""
        raise NotImplementedError()

    def generate(self, relname):
        """Generate code for module ``relname``.

        Should call `store_contents` for any files generated.
        """
        raise NotImplementedError()
