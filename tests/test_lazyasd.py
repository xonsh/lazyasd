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
    s = "test"
    lo = LazyObject(lambda: s, {}, 'lo')
    assert lo + s == 2*s
