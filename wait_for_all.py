import config
import io
import json
import os.path
import sys
import datetime
import time
import yaml
import compatibility
import common
import auth
import helper
import duplicati_client
import time

from os.path import expanduser
from os.path import splitext
from requests_wrapper import requests_wrapper as requests

url = sys.argv[1]
password = sys.argv[2]

# Default values
data = {
    "last_login": None,
    "parameters_file": None,
    "server": {
        "port": "",
        "protocol": "http",
        "url": "localhost",
        "verify": True
    },
    'token': None,
    'token_expires': None,
    'verbose': False,
    'precise': False,
    'authorization': ''
}

# Detect home dir for config file
config.CONFIG_FILE = compatibility.get_config_location()

# Load configuration
overwrite = False
data = duplicati_client.load_config(data, overwrite)

param_file = None

basic_user = None
basic_pass = None
certfile = None
insecure = False
verify = auth.determine_ssl_validation(data, certfile, insecure)
interactive = False
data = auth.login(data, url, password, verify, interactive,
                  basic_user, basic_pass)


while True:
    data = auth.login(data, url, password, verify, interactive,
                      basic_user, basic_pass)
    resource_list = duplicati_client.fetch_backup_list(data)

    wait = False
    for entry in resource_list:
        if "Progress" in entry:
            prog = entry["Progress"]
            tid = prog["TaskID"]
            print(prog)
            wait = True

    if wait:
        time.sleep(15)
    else:
        break
