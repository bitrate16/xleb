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


import logging

import aiohttp.web
import aiohttp.web_exceptions

from xleb.config import config
from xleb.state import state


def access_check_whitelisted(path: str) -> bool:
    """Check if specific path is accessible without auth"""

    if path.startswith((
        '/css/',
        '/media/'
    )):
        return True

    return False


@aiohttp.web.middleware
async def access_check(request: aiohttp.web.Request, handler):
    """Check if user password is valid and provide access. Else return auth page"""

    password = request.cookies.get('xleb-password', None)
    if config.password is None or password == config.password or access_check_whitelisted(request.path):
        # pass authorized flag
        request['authorized'] = True
        return await handler(request)

    if request.path == '/':
        # pass unauthorized flag
        request['authorized'] = False
        return await handler(request)

    raise aiohttp.web_exceptions.HTTPUnauthorized()

@aiohttp.web.middleware
async def log_request(request: aiohttp.web.Request, handler):
    logging.info(f'{ request.method } { request.path_qs }')
    return await handler(request)
