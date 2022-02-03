"""Tests lazy and self destruictive objects."""
from lazyasd import LazyObject, load_module_in_background

#
# LazyObject Tests
#

def test_lazyobject_getitem():
    lo = LazyObject(lambda: {'x': 1}, {}, 'lo')
    assert 1 == lo['x']


def test_bg_load():
    load_module_in_background('pkg_resources')
    import pkg_resources
    pkg_resources.iter_entry_points

def test_lazyobject_plus():
    a, s = "a ", "test"
    lo = LazyObject(lambda: a, {}, 'lo')
    assert lo + s == a + s
    assert s + lo == s + a
