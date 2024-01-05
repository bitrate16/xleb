import pathlib
import os

from xleb.config import config


def normalize_webpath(webpath: str) -> str:
    # Leading '/'
    while len(webpath) > 1 and webpath.startswith('/'):
        webpath = webpath[1:]

    # Trailing '/'
    while len(webpath) > 1 and webpath.endswith('/'):
        webpath = webpath[:-1]

    # normalize
    webpath = webpath.strip()
    if not webpath.startswith('/'):
        webpath = '/' + webpath

    # normalize to posix-style path
    return pathlib.Path(webpath).resolve(strict=False).as_posix()


def get_fspath_from_webpath(webpath: str) -> str:

    # normalize to posix-style path
    webpath = normalize_webpath(webpath)

    # Get fs path
    return os.path.join(config.path, webpath[1:])


def is_valid_subpath(fspath: str) -> bool:
    """Check if `'/s/b'` is subpath of `config.path = '/a'`"""

    return fspath.startswith(config.path + '/')
