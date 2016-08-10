import sys
from textwrap import dedent

from datadiff import tools

from nose.tools import assert_raises, assert_equal


def test_assert_equal_true():
    # nothing raised
    assert_equal(None, tools.assert_equals(7, 7))
    
def test_assert_equal_false():
    try:
        tools.assert_equals([3,4], [5,6])
    except:
        e = sys.exc_info()[1]
        assert_equal(type(e), AssertionError)
        assert_equal(str(e), dedent('''\
            
            --- a
            +++ b
            [
            @@ -0,1 +0,1 @@
            -3,
            -4,
            +5,
            +6,
            ]'''))
    else:
        raise AssertionError("Should've raised an AssertionError")
    
def test_assert_equal_msg():
    try:
        tools.assert_equals(3, 4, "whoops")
    except:
        e = sys.exc_info()[1]
        assert_equal(type(e), AssertionError,
                     "Raised exception should be AssertionError")
        assert_equal(str(e), "whoops")
    else:
        raise AssertionError("Should've raised an AssertionError")
    
def test_assert_equals():
    assert_equal(tools.assert_equal, tools.assert_equals)

def test_assert_equal_simple():
    try:
        tools.assert_equals(True, False)
    except:
        e = sys.exc_info()[1]
        assert_equal(type(e), AssertionError)
        assert_equal(str(e), dedent('''\
            True != False'''))
    else:
        raise AssertionError("Should've raised an AssertionError")

def test_assert_equal_simple_types():
    try:
        tools.assert_equals('a', 7)
    except:
        e = sys.exc_info()[1]
        assert_equal(type(e), AssertionError)
        assert_equal(str(e), dedent('''\
            'a' != 7'''))
    else:
        raise AssertionError("Should've raised an AssertionError")

def test_assert_almost_equal():
    tools.assertAlmostEqual([1.0], [1.0])
    tools.assertAlmostEqual([1.0], [1.000000001])
    tools.assertAlmostEqual([1.0], [1.00001], places=4)
    tools.assertAlmostEqual({"k": 1.0}, {"k": 1.00001}, places=4)
    tools.assertAlmostEqual({1.0}, {1.00001}, places=4)

def test_assert_not_almost_equal():
    assert_raises(AssertionError, tools.assertAlmostEqual, [1.0], [1.00001])
    assert_raises(AssertionError, tools.assertAlmostEqual, [1.0], [1.0001], places=4)
    assert_raises(AssertionError, tools.assertAlmostEqual, {"k": 1.0}, {"k": 1.1}, places=4)
    assert_raises(AssertionError, tools.assertAlmostEqual, {1.0}, {1.1}, places=4)

if __name__ == '__main__':
    try:
        import nose
    except (ImportError, SyntaxError, NameError):
        pass
    else:
        nose.main()
        sys.exit(0)
    
    import types
    for fn_name, fn in sorted(locals().items()):
        if fn_name.startswith('test_') and type(fn) == types.FunctionType:
            sys.stderr.write(fn_name + '...\n')
            fn()
