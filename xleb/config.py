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


import argparse
import inspect
import os

from typing import List, Optional


def get_args() -> dict:
    """Get commandline arguments"""

    parser = argparse.ArgumentParser('xleb')

    parser.add_argument(
        '--path', '-d',
        help='root workdir',
        type=str,
        default='.',
    )

    parser.add_argument(
        '--port', '-p',
        help='server port',
        type=int,
        default=9876,
    )

    parser.add_argument(
        '--host', '-a',
        help='server address',
        type=str,
        default='0.0.0.0',
    )

    parser.add_argument(
        '--log-level', '-e',
        help='logging log level',
        type=str,
        default='INFO',
    )

    parser.add_argument(
        '--log', '-l',
        help='enable logging',
        action='store_true',
    )

    parser.add_argument(
        '--password', '-s',
        help='user password',
        type=str,
        default=None,
    )

    parser.add_argument(
        '--origins', '-r',
        help='allowed origins for cors. by default allows all',
        nargs='+',
        type=str,
        default=[],
    )

    return vars(parser.parse_args())


class XlebConfig:
    """Container for arguments with autoinflate from on-disk config or cmdline config"""

    def __init__(
        self,
        path: str='.',
        port: int=9876,
        host: str='0.0.0.0',
        log_level: str='INFO',
        log: bool=False,
        password: Optional[str]=None,
        origins: List[str]=None,
    ):
        self.path = os.path.abspath(path)
        self.port = port
        self.host = host
        self.log_level = log_level.upper()
        self.log = log
        self.password = password
        self.origins = origins

    @staticmethod
    def init():
        # Get config from commandline arguments
        config = get_args()

        keys = inspect.signature(XlebConfig).parameters.keys()
        return XlebConfig(
            **{ k: config[k] for k in keys if k in config and config[k] is not None }
        )

config = XlebConfig.init()
