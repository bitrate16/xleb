import os
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

    passhash = request.cookies.get('xleb-passhash', None)
    if config.passhash is None or passhash == config.passhash or access_check_whitelisted(request.path):
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
