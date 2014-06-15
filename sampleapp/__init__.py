import logging
import logging.config
import os
import sys
from mongoengine import connect

# Work around for CentOS 6 in regard to how Jinja2-2.6 is packaged
if os.path.exists("/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg"):
    sys.path.insert(0, "/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg")
from flask import Flask, jsonify

LOG_CONFIG_FILE="/etc/sampleapp/logging.cfg" 
DB_NAME="sampleapp"

# app instantiation needs to be before the "from sampleapp import api"
# circular reference is in play here
app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

from sampleapp import api

@app.route("/site-map")
def site_map():
    """
    Returns all URLs configured in this application
    """
    endpoints = []
    for rule in app.url_map.iter_rules():
        info = {}
        info["endpoint"] = str(rule)
        info["methods"] = str(rule.methods)
        info["arguments"] = str(rule.arguments)
        info["defaults"] = str(rule.defaults)
        endpoints.append(info)
    return jsonify(result={"endpoints": endpoints})


def configure_logging(log_config_file):
    if not os.access(log_config_file, os.R_OK):
        raise RuntimeError("Unable to read log configuration file: %s" % (log_config_file))
    logging.config.fileConfig(log_config_file)

##
# App Initialization
##
def initialize(db_name=None, log_config_file=None):
    if not db_name:
        db_name = DB_NAME
    if not log_config_file:
        log_config_file = LOG_CONFIG_FILE
    configure_logging(log_config_file)
    db = connect(db_name)
