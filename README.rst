=======
lazyasd
=======
A package that provides lazy and self-destructive tools for speeding up module
imports. This is useful whenever startup times are critical, such as for
command line interfaces or other user-facing applications.

The tools in this module implement two distinct strategies for speeding up
module import. The first is delayed construction of global state and the
second is to import expensive modules in a background thread.

Lazy Construction
-----------------
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
``"foo"`` using regular expressions. The naive version is slow, per function
call, because it has to construct the regex each time::

    import re

    def has_foo(s):
        return re.search('foo', )
