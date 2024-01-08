import pathlib
import os

from xleb.config import config


def normalize_abs_posixpath(posixpath: str) -> str:
    """
    Normalize posix pah and expect it to be absolute. If path does not start
    with `'/'`, it is appended. Excessive leading or trailing `'/'` are trimmed.
    If path starts with up jump `'..'` or `'/..'`, they are ignored.

    `posixpath` - path that will be converted to posix path starting from `'/'`.
    """

    posixpath = posixpath.strip()

    # Leading '/' + unmeant spaces
    while posixpath.startswith(('/', ' ')):
        posixpath = posixpath[1:]

    # Trailing '/' + unmeant spaces
    while posixpath.endswith(('/', ' ')):
        posixpath = posixpath[:-1]

    # normalize
    posixpath = posixpath.strip()
    if not posixpath.startswith('/'):
        posixpath = '/' + posixpath

    # normalize to posix-style path
    return pathlib.Path(posixpath).resolve(strict=False).as_posix()


def posixpath_to_fspath(posixpath: str, rootpath: str=config.path) -> str:
    """
    Convert posix path to fs path relative to `rootpath`. Result path can not
    go beyond `rootpath` to prevent malicious filesystem access. This means
    than if `rootpath = '/home/user'` and `posixpath = '../../etc/passwd'`,
    result path will be `/home/user/etc/passwd'`. `rootpath` is automatically
    resolved to absolute path with `os.path.abspath`.

    This function produces safe fspath and prevents travelling over

    `posixpath` - path that will be converted to posix path using
    `normalize_abs_posixpath`

    `rootpath` - real filesystem path too look in, will be converted to absolute
    using `os.path.abspath`.
    """

    rootpath = os.path.abspath(rootpath)

    # normalize to posix-style path
    posixpath = normalize_abs_posixpath(posixpath)

    # Root path only
    if posixpath == '/':
        return rootpath

    # Get fs path relative to root
    return os.path.abspath(os.path.join(rootpath, posixpath[1:]))


def is_safe_fspath(fspath: str, rootpath: str=config.path) -> bool:
    """
    Check if `fspath` is relative to `rootpath` to prevent unsafe traversal.
    `rootpath` is automatically resolved to absolute path with `os.path.abspath`.

    `fspath` - real filesystem path to check, will be processed with
    `os.path.abspath`.

    `rootpath` - real filesystem path too look in, will be converted to absolute
    using `os.path.abspath`.
    """

    fspath = os.path.abspath(fspath)
    rootpath = os.path.abspath(rootpath)

    return fspath == rootpath or fspath.startswith(rootpath + os.path.sep)
