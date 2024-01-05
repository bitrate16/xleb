import argparse
import inspect
import hashlib
import os


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
        default='127.0.0.1',
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

    return vars(parser.parse_args())


class XlebConfig:
    """Container for arguments with autoinflate from on-disk config or cmdline config"""

    def __init__(
        self,
        path: str='.',
        port: int=8000,
        host: str='127.0.0.1',
        log_level: str='INFO',
        log: bool=False,
        password: str=None,
    ):
        self.path = os.path.abspath(path)
        self.port = port
        self.host = host
        self.log_level = log_level
        self.log = log
        self.passhash = hashlib.sha256(password.encode()).hexdigest() if password is not None else None

    @staticmethod
    def init():
        # Get config from commandline arguments
        config = get_args()

        keys = inspect.signature(XlebConfig).parameters.keys()
        return XlebConfig(
            **{ k: config[k] for k in keys if k in config and config[k] is not None }
        )

config = XlebConfig.init()
