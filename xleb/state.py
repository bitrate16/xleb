import aiohttp
import aiohttp.web


class XlebState:
    """Global state"""

    app: aiohttp.web.Application = None
    routes: aiohttp.web.RouteTableDef = None
    moddir: str = None

state = XlebState()
