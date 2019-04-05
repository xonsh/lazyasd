"""Tests lazy and self destruictive objects."""
from lazyasd import LazyObject, load_module_in_background,\
        BackgroundModuleDelayNoop, BackgroundModuleDelayExpBackoff,\
        BackgroundModuleDelayConst, BackgroundModuleDelayEvent

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

def test_bg_load_delay_noop():
    load_module_in_background('pkg_resources', delayobj=BackgroundModuleDelayNoop())
    import pkg_resources
    pkg_resources.iter_entry_points

def test_bg_load_delay_expbackoff():
    load_module_in_background('pkg_resources', delayobj=BackgroundModuleDelayExpBackoff(5, 1, 2))
    import pkg_resources
    pkg_resources.iter_entry_points

def test_bg_load_delay_const():
    load_module_in_background('pkg_resources', delayobj=BackgroundModuleDelayConst(50))
    import pkg_resources
    pkg_resources.iter_entry_points

def test_bg_load_delay_event():
    delayobj=BackgroundModuleDelayEvent(50)
    ev = delayobj.get_event()
    load_module_in_background('pkg_resources', delayobj=delayobj)
    ev.set()
    import pkg_resources
    pkg_resources.iter_entry_points
