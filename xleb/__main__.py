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


import os
import logging

import aiohttp
import aiohttp.web
import aiohttp.hdrs
import aiohttp.web_exceptions

import aiohttp_middlewares

from xleb.state import state
from xleb.config import config


def main():

    # Prepare logging
    logging.basicConfig(
        level=config.log_level,
        format='[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.getLogger().disabled = not config.log

    # Prepare application
    state.app = aiohttp.web.Application()
    state.routes = aiohttp.web.RouteTableDef()
    state.moddir = os.path.dirname(__file__)

    logging.debug(f'state.moddir = "{ state.moddir }"')


    # prepare endpoints
    import xleb.fapi

    # Middlewares
    import xleb.fmiddleware

    if config.origins:
        import re
        origins = [
            origin if '*' not in origin else re.compile(origin.replace('.', '\\.').replace('*', '.*'))
            for origin in config.origins
        ]
        print(origins)
        state.app.middlewares.append(aiohttp_middlewares.cors_middleware(
            origins=origins,
            allow_methods=[ 'GET', 'POST' ],
            allow_headers=[ '*' ],
            allow_credentials=True
        ))
    else:
        state.app.middlewares.append(aiohttp_middlewares.cors_middleware(
            allow_all=True
        ))
    state.app.middlewares.append(xleb.fmiddleware.log_request)
    state.app.middlewares.append(xleb.fmiddleware.access_check)

    # Routes bind
    state.app.add_routes(state.routes)

    # Start app
    aiohttp.web.run_app(
        app=state.app,
        host=config.host,
        port=config.port,
        access_log=None,
    )

if __name__ == '__main__':
    main()
