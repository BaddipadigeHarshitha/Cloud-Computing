import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/ubuntu/myflaskapp")

from flaskapp import app as application
