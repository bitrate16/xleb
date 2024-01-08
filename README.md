# Xleb

![screenshot](screenshot.png)

web-based remote file manager

# What is it?

Xleb is a single-module python utility used to browse and manage files on rempote host with support of:
* File upload/download including drap & drop
* File delete
* File move/rename
* File listing
* WEB UI with or without password

# Install

Install with

```bash
pip install xleb
```

# How to use

Use as module

```bash
python -m xleb
```

or directly

```
$ xleb -h
usage: xleb [-h] [--path PATH] [--port PORT] [--host HOST] [--log-level LOG_LEVEL] [--log] [--password PASSWORD] [--origins ORIGINS [ORIGINS ...]]

options:
  -h, --help            show this help message and exit
  --path PATH, -d PATH  root workdir
  --port PORT, -p PORT  server port
  --host HOST, -a HOST  server address
  --log-level LOG_LEVEL, -e LOG_LEVEL
                        logging log level
  --log, -l             enable logging
  --password PASSWORD, -s PASSWORD
                        user password
  --origins ORIGINS [ORIGINS ...], -r ORIGINS [ORIGINS ...]
                        allowed origins for cors. by default allows all
```

# Notes

* password is sent and stored inside cookie without hashing due to lack of built-in hashing algorightms in vanilla javascript
* password (from cookie) is used as auth for every action
* by default CORS allows everything
* if file exists during upload, it is ignored and untouched on server

# LICENSE

```
xleb - web-based remote file manager
Copyright (C) 2024  bitrate16

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```