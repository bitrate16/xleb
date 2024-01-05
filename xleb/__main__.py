import os
import logging

import aiohttp
import aiohttp.web
import aiohttp.hdrs
import aiohttp.web_exceptions

from xleb.state import state
from xleb.config import config


def main():

    # Prepare logging
    logging.basicConfig(
        level=config.log_level,
        format='[%(asctime)s.%(msecs)03d] %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.getLogger().disabled = not config.log

    # Prepare application
    state.app = aiohttp.web.Application()
    state.routes = aiohttp.web.RouteTableDef()
    state.moddir = os.path.dirname(__file__)

    logging.debug(f'passhash = { config.passhash }')

    logging.debug(f'state.moddir = "{ state.moddir }"')


    # prepare endpoints
    import xleb.fapi

    # Middlewares
    import xleb.fmiddleware
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
