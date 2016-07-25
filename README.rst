=======
lazyasd
=======
A package that provides lazy and self-destructive tools for speeding up module
imports. This is useful whenever startup times are critical, such as for
command line interfaces or other user-facing applications.

The tools in this module implement two distinct strategies for speeding up
module import. The first is delayed construction of global state and the
second is to import expensive modules in a background thread.

Feel free to use lazyasd as a dependency or, because it is implemented as a
single module, copy the ``lazyasd.py`` file into your project.

Lazy Construction
*****************
Many operations related to data construction or inspection setup can take
a long time to complete. If only a single copy of the data or a cached
representation is needed, in Python it is common to move the data to the
global or module level scope.

By moving to module level, we help ensure that only a single copy of the data
is ever built.  However, by moving to module scope, the single perfomance hit
now comes at import time. This is itself wasteful if the data is never used.
Furthermore, the more data that is built globally, the longer importing the
module takes.

For example, consider a function that reports if a string contains the word
``"foo"`` using regular expressions. The naive version is relatively slow, per
function call, because it has to construct the regex each time:

.. code-block:: python

    import re

    def has_foo_simple(s):
        return re.search('foo', s) is not None

The standard way of improving performance is to compile the regex at global
scope. Rewriting, we would see:

.. code-block:: python

    import re

    FOO_RE = re.compile('foo')

    def has_foo_compiled(s):
        return FOO_RE.search(s) is not None

Now, each call of ``has_foo_compiled()`` is much faster than a call of
``has_foo_simple()`` because we have shifted the compiliation to import
time.  But what if we never actually call ``has_foo()``? In this case,
the original version was better because the imports are fast.

Having the best of both compile-once and don't-compile-on-import is where
the lazy and self-destructive tools come in.  A ``LazyObject`` instance
has a loader function, a context to place the result of the into, and the
name of the loaded value in the context. The ``LazyObject`` does no
work when it is first created.  However, whenever an attribute is accessed
(or a variety of other operations) the loader will be called, the true
value will be constructed, and the ``LazyObject`` will act as a proxy to
loaded object.

Using the above regex example, we have minimal import-time and run-time
perfomance hits with the following lazy implementation:

.. code-block:: python

    import re
    from lazyasd import LazyObject

    FOO_RE = LazyObject(lambda: re.compile('foo'), globals(), 'FOO_RE')

    def has_foo_lazy(s):
        return FOO_RE.search(s) is not None

To walk through the above, at import time ``FOO_RE`` is a LazyObject, that has a
lambda loader which returns the regex we care about.  If ``FOO_RE`` is never
accessed this is how it will remain.  However, the first time ``has_foo_lazy()``
is called, accessing the ``search`` method will cause the ``LazyObject`` to:

1. Call the loader (getting ``re.compile('foo')`` as the result)
2. Place the result in the context, eg ``globals()['FOO_RE'] = re.compile('foo')``
3. Look up attributes and methods (such as ``search``) on the result.

Now because of the context replacement, ``FOO_RE`` now is a regular expression
object. Further calls to ``has_foo_lazy()`` will see ``FOO_RE`` as a regular
expression object directly, and not as a ``LazyObject``.  In fact, if no lingering
refences remain, the original ``LazyObject`` instance can be totally cleaned up
by the garbage collector!

For the truly lazy, there is also a ``lazyobject`` decorator:

.. code-block:: python

    import re
    from lazyasd import lazyobject

    @lazyobject
    def foo_re():
        return re.compile('foo')

    def has_foo_lazy(s):
        return foo_re.search(s) is not None

Another useful pattern is to implement lazy module imports, where the
module is only imported if a member of it used:

.. code-block:: python

    import importlib
    from lazyasd import lazyobject

    @lazyobject
    def os():
        return importlib.import_module('os')

The world is beautifully yours, but feel free to take a nap first.

Specific Laziness
-----------------
The ``LazyBool`` class and ``lazybool`` decorator have the same interface as
lazy objects.  These are provided for objects that are intended to be resolved
as booleans.

The ``LazyDict`` class and ``lazydict`` decorator are similar.  Here however,
the first value is a dictionary of key-loaders.  Rather than having a single
loader, each value is loaded individually when its key is first accessed.


Background Imports
******************
Even with all of the above laziness, sometimes it isn't enough. Sometimes a
module is so painful to import and so unavoidable that you need to import
it on background thread so that the rest of the application can boot up
in the meantime. This is the purpose of ``load_module_in_background()``.

For example, if you are using pygments and you want the import to safely
be 100x faster, simply drop in the following lines:

.. code-block:: python

    # must come before pygments imports
    from lazyasd import load_module_in_background
    load_module_in_background('pkg_resources',
                              replacements={'pygments.plugin': 'pkg_resources'})

    # now pygments is fast to import
    from pygments.style import Style

This prevents ``pkg_resources``, which comes from setuptools, from searching your
entire filesystem for plugins at import time. Like above, this import acts as
proxy and will block until it is needed.  It is also robust if the module has
already been imported. In some cases, this background importing is the best a
third party application can do.

