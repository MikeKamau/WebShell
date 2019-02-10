#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/mike/webshell')
from webshell import app as application
application.secret_key = 'l\xf6\xa4\xd4\xb8\xaf\x10\xb1\xb5\xf0j\xa7\xa5\xf1q\n6Mz\xf6T\xa3GjB]A\xa8\xc5\xf2\x05\x1d'
