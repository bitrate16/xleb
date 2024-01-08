import xleb.pathutils

from xleb.config import config


def test_normalize_abs_posixpath():
    """Test pathutils webpath normalization"""

    assert xleb.pathutils.normalize_abs_posixpath('') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('/') == '/'

    assert xleb.pathutils.normalize_abs_posixpath('       ') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('    /  ') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('  //// ') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('///////') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('/ / / /') == '/'
    assert xleb.pathutils.normalize_abs_posixpath(' // /  ') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('///////foo') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('/// ///foo') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('///////foo/') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('//// / foo/') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('       foo/') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('       foo ') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('/foo/////') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('///////foo////') == '/foo'

    assert xleb.pathutils.normalize_abs_posixpath('foo') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('/foo') == '/foo'

    assert xleb.pathutils.normalize_abs_posixpath('foo/bar') == '/foo/bar'
    assert xleb.pathutils.normalize_abs_posixpath('/foo/bar') == '/foo/bar'

    assert xleb.pathutils.normalize_abs_posixpath('foo/../bar') == '/bar'
    assert xleb.pathutils.normalize_abs_posixpath('/foo/../bar') == '/bar'

    assert xleb.pathutils.normalize_abs_posixpath('..') == '/'
    assert xleb.pathutils.normalize_abs_posixpath('/..') == '/'

    assert xleb.pathutils.normalize_abs_posixpath('../foo') == '/foo'
    assert xleb.pathutils.normalize_abs_posixpath('/../foo') == '/foo'


def test_posixpath_to_fspath():
    """Test pathutils webpath to fspath"""

    rootpath = '/foo/bar'

    assert xleb.pathutils.posixpath_to_fspath('', rootpath=rootpath) == '/foo/bar'
    assert xleb.pathutils.posixpath_to_fspath('/', rootpath=rootpath) == '/foo/bar'

    assert xleb.pathutils.posixpath_to_fspath('baz', rootpath=rootpath) == '/foo/bar/baz'
    assert xleb.pathutils.posixpath_to_fspath('/baz', rootpath=rootpath) == '/foo/bar/baz'

    assert xleb.pathutils.posixpath_to_fspath('baz/taz', rootpath=rootpath) == '/foo/bar/baz/taz'
    assert xleb.pathutils.posixpath_to_fspath('/baz/taz', rootpath=rootpath) == '/foo/bar/baz/taz'

    assert xleb.pathutils.posixpath_to_fspath('baz/../taz', rootpath=rootpath) == '/foo/bar/taz'
    assert xleb.pathutils.posixpath_to_fspath('/baz/../taz', rootpath=rootpath) == '/foo/bar/taz'

    assert xleb.pathutils.posixpath_to_fspath('..', rootpath=rootpath) == '/foo/bar'
    assert xleb.pathutils.posixpath_to_fspath('/..', rootpath=rootpath) == '/foo/bar'

    assert xleb.pathutils.posixpath_to_fspath('../taz', rootpath=rootpath) == '/foo/bar/taz'
    assert xleb.pathutils.posixpath_to_fspath('/../taz', rootpath=rootpath) == '/foo/bar/taz'

    rootpath = '/foo/bar/'

    assert xleb.pathutils.posixpath_to_fspath('', rootpath=rootpath) == '/foo/bar'
    assert xleb.pathutils.posixpath_to_fspath('/', rootpath=rootpath) == '/foo/bar'

    assert xleb.pathutils.posixpath_to_fspath('baz', rootpath=rootpath) == '/foo/bar/baz'
    assert xleb.pathutils.posixpath_to_fspath('/baz', rootpath=rootpath) == '/foo/bar/baz'

    assert xleb.pathutils.posixpath_to_fspath('baz/taz', rootpath=rootpath) == '/foo/bar/baz/taz'
    assert xleb.pathutils.posixpath_to_fspath('/baz/taz', rootpath=rootpath) == '/foo/bar/baz/taz'

    assert xleb.pathutils.posixpath_to_fspath('baz/../taz', rootpath=rootpath) == '/foo/bar/taz'
    assert xleb.pathutils.posixpath_to_fspath('/baz/../taz', rootpath=rootpath) == '/foo/bar/taz'

    assert xleb.pathutils.posixpath_to_fspath('..', rootpath=rootpath) == '/foo/bar'
    assert xleb.pathutils.posixpath_to_fspath('/..', rootpath=rootpath) == '/foo/bar'

    assert xleb.pathutils.posixpath_to_fspath('../taz', rootpath=rootpath) == '/foo/bar/taz'
    assert xleb.pathutils.posixpath_to_fspath('/../taz', rootpath=rootpath) == '/foo/bar/taz'


def test_is_safe_path():
    """Test if given path is safe relative to the given rootdir"""

    rootpath = '/foo/bar'

    assert xleb.pathutils.is_safe_fspath('/foo/bar', rootpath=rootpath) == True
    assert xleb.pathutils.is_safe_fspath('/foo/bar/', rootpath=rootpath) == True

    assert xleb.pathutils.is_safe_fspath('/foo', rootpath=rootpath) == False
    assert xleb.pathutils.is_safe_fspath('/foo/', rootpath=rootpath) == False

    assert xleb.pathutils.is_safe_fspath('./foo', rootpath=rootpath) == False
    assert xleb.pathutils.is_safe_fspath('./foo/', rootpath=rootpath) == False

    assert xleb.pathutils.is_safe_fspath('../foo', rootpath=rootpath) == False
    assert xleb.pathutils.is_safe_fspath('../foo/', rootpath=rootpath) == False

    assert xleb.pathutils.is_safe_fspath('~/foo', rootpath=rootpath) == False
    assert xleb.pathutils.is_safe_fspath('~/foo/', rootpath=rootpath) == False
