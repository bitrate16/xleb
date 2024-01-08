# xleb - web-based remote file manager
# Copyright (C) 2024  bitrate16
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import re
import os
import shutil
import pathlib
import logging

import aiohttp
import aiohttp.web
import aiohttp.web_exceptions

import xleb.pathutils

from xleb.state import state
from xleb.config import config


# Test if given string is valid file/directory name
FS_NODE_TEST_RE = re.compile(r'^(?!^(?:PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d)(?:\..+)?$)(?:\.*?(?!\.))[^\x00-\x1f\\?*:\";|\/<>]+(?<![\s.])$')


# Plain API definition
# --------------------

@state.routes.get('/css/{tail:.*}')
async def handle_css(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Getter for `/css/` directory"""

    # Core dir
    dir = os.path.join(state.moddir, 'static/css')

    # Get fspath for posixpath
    file_path = xleb.pathutils.posixpath_to_fspath(request.match_info['tail'], rootpath=dir)

    # Check for existing
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return aiohttp.web.FileResponse(file_path)

    raise aiohttp.web_exceptions.HTTPNotFound()


@state.routes.get('/media/{tail:.*}')
async def handle_media(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Getter for `/media/` directory"""

    # Core dir
    dir = os.path.join(state.moddir, 'static/media')

    # Get fspath for posixpath
    file_path = xleb.pathutils.posixpath_to_fspath(request.match_info['tail'], rootpath=dir)

    # Check for existing
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return aiohttp.web.FileResponse(file_path)

    raise aiohttp.web_exceptions.HTTPNotFound()


@state.routes.get('/')
async def handle_root(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Return index page depending on authorized state"""

    if not request['authorized']:
        return aiohttp.web.FileResponse(os.path.join(state.moddir, 'static/auth.html'))
    return aiohttp.web.FileResponse(os.path.join(state.moddir, 'static/index.html'))


@state.routes.get('/list')
async def api_list(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """directory listing"""

    webpath = request.query.get('path', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # normalize to posix-style path
    webpath = xleb.pathutils.normalize_abs_posixpath(webpath)

    # Get fs path
    fspath = xleb.pathutils.posixpath_to_fspath(webpath)

    # Check subdir
    if not xleb.pathutils.is_safe_fspath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    if not os.path.exists(fspath) or not os.path.isdir(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    fs_files = os.listdir(fspath)
    files = []

    for name in fs_files:
        if webpath == '/':
            web_filepath = f'/{ name }'
        else:
            web_filepath = f'{ webpath }/{ name }'

        fs_filepath = os.path.join(fspath, name)

        is_file = os.path.isfile(fs_filepath)
        is_dir = os.path.isdir(fs_filepath)

        files.append({
            'path': web_filepath,
            'name': name,
            'is_file': is_file,
            'is_dir': is_dir,
            'size': None if not is_file else os.stat(fs_filepath).st_size,
        })

    return aiohttp.web.json_response({
        'files': files,
    })


@state.routes.get('/download')
async def handle_download(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Direct file download"""

    webpath = request.query.get('path', None)

    if webpath is None:
        raise aiohttp.web_exceptions.HTTPNotFound()

    # normalize to posix-style path
    webpath = xleb.pathutils.normalize_abs_posixpath(webpath)

    # Get fs path
    fspath = xleb.pathutils.posixpath_to_fspath(webpath)

    # Check subdir
    if not xleb.pathutils.is_safe_fspath(fspath):
        raise aiohttp.web_exceptions.HTTPNotFound()

    if not os.path.exists(fspath):
        raise aiohttp.web_exceptions.HTTPNotFound()

    return aiohttp.web.FileResponse(fspath)


@state.routes.get('/move')
async def handle_move(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Move file or directory from any path to any path"""

    websrcpath = request.query.get('src_path', None)
    webdstpath = request.query.get('dst_path', None)

    if websrcpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid src_path',
        })

    if webdstpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid dst_path',
        })

    websrcpath = xleb.pathutils.normalize_abs_posixpath(websrcpath)
    webdstpath = xleb.pathutils.normalize_abs_posixpath(webdstpath)

    fssrcpath = xleb.pathutils.posixpath_to_fspath(websrcpath)
    fsdstpath = xleb.pathutils.posixpath_to_fspath(webdstpath)

    # Check subdirs
    if not xleb.pathutils.is_safe_fspath(fssrcpath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    if not xleb.pathutils.is_safe_fspath(fsdstpath):
        return aiohttp.web.json_response({
            'error': 'invalid dst_path'
        })

    # Check existing
    if not os.path.exists(fssrcpath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Actually move (how?)
    try:
        os.renames(fssrcpath, fsdstpath)
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'move failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


@state.routes.get('/delete')
async def handle_delete(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Delete file or directory"""

    webpath = request.query.get('path', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid src_path',
        })

    webpath = xleb.pathutils.normalize_abs_posixpath(webpath)

    fspath = xleb.pathutils.posixpath_to_fspath(webpath)

    # Check subdirs
    if not xleb.pathutils.is_safe_fspath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Check existing
    if not os.path.exists(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Actually move (how?)
    try:
        if os.path.isdir(fspath):
            shutil.rmtree(fspath)
        else:
            os.remove(fspath)
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'delete failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


@state.routes.get('/mkdir')
async def handle_mkdir(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Create directory"""

    webpath = request.query.get('path', None)
    name = request.query.get('name', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid path',
        })

    if not FS_NODE_TEST_RE.match(name):
        return aiohttp.web.json_response({
            'error': 'invalid name',
        })

    webpath = xleb.pathutils.normalize_abs_posixpath(webpath)

    fspath = xleb.pathutils.posixpath_to_fspath(webpath)

    # Check subdirs
    if not xleb.pathutils.is_safe_fspath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # Check existing
    if not os.path.exists(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # Actually move (how?)
    try:
        os.makedirs(os.path.join(fspath, name))
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'delete failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


@state.routes.post('/upload')
async def handle_upload(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Upload file in given directory"""

    webpath = request.query.get('path', None)

    if webpath is None:
        raise aiohttp.web.HTTPBadRequest()

    webpath = xleb.pathutils.normalize_abs_posixpath(webpath)

    fspath = xleb.pathutils.posixpath_to_fspath(webpath)

    # Check subdirs
    if not xleb.pathutils.is_safe_fspath(fspath):
        raise aiohttp.web.HTTPBadRequest()

    # Check existing
    if not os.path.exists(fspath):
        raise aiohttp.web.HTTPBadRequest()

    # Form iterator
    try:
        reader = await request.multipart()

        field = None
        while not reader.at_eof():
            local_field = await reader.next()
            if local_field.name == 'file':
                field = local_field
                break
    except Exception as e:
        logging.error(e, exc_info=True)
        raise aiohttp.web.HTTPInternalServerError()

    # Field check
    if field is None:
        raise aiohttp.web.HTTPBadRequest()

    # File check
    filename = field.filename
    if filename is None:
        raise aiohttp.web.HTTPBadRequest()

    filename = filename.strip()
    if not filename:
        raise aiohttp.web.HTTPBadRequest()

    if not FS_NODE_TEST_RE.match(filename):
        raise aiohttp.web.HTTPBadRequest()

    fspath = os.path.join(fspath, filename)

    # Prevent duplicates
    if os.path.exists(fspath):
        raise aiohttp.web.HTTPConflict()

    # Receive
    try:
        with open(fspath, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)

        return aiohttp.web.Response()
    except Exception as e:
        logging.error(e, exc_info=True)
        try:
            os.remove(fspath)
        except:
            pass

        raise aiohttp.web.HTTPInternalServerError()
