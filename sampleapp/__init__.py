import logging
import logging.config
import os
import sys
from ConfigParser import SafeConfigParser
from mongoengine import connect

# Work around for CentOS 6 in regard to how Jinja2-2.6 is packaged
if os.path.exists("/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg"):
    sys.path.insert(0, "/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg")
from flask import Flask, jsonify

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

##
# Configuration
##
CONFIG = None # ConfigParser.SafeConfigParser instance
CONFIG_DEFAULT_FILE = "/etc/sampleapp/sampleapp.cfg"
CONFIG_DEFAULT_VALUES = {
    'database': {
        'name': 'sampleapp',
        'host': 'localhost',
        'port': '27017',
    },
    'logs': {
        'config': '/etc/sampleapp/logging.cfg',
    },
}

def check_config_file(config_file):
    if not os.access(config_file, os.F_OK):
        raise RuntimeError('Cannot find configuration file: %s' % config_file)
    if not os.access(config_file, os.R_OK):
        raise RuntimeError('Cannot read configuration file: %s' % config_file)
    return True


def load_configuration(config_file):
    global CONFIG
    check_config_file(config_file)
    CONFIG = SafeConfigParser()
    # add the defaults first
    for section, settings in CONFIG_DEFAULT_VALUES.items():
        CONFIG.add_section(section)
        for option, value in settings.items():
            CONFIG.set(section, option, value)
    # read the config files
    return CONFIG.read([config_file])


def configure_logging(log_config_file):
    if not os.access(log_config_file, os.R_OK):
        raise RuntimeError("Unable to read log configuration file: %s" % (log_config_file))
    logging.config.fileConfig(log_config_file)


##
# App Initialization
##
def initialize(config_file=None):
    global log

    if not config_file:
        config_file = CONFIG_DEFAULT_FILE
    load_configuration(config_file)
    
    db_name = CONFIG.get("database", "name")
    db_host = CONFIG.get("database", "host")
    db_port = CONFIG.getint("database", "port")
    log_config_file = CONFIG.get("logs", "config")

    configure_logging(log_config_file)
    log = logging.getLogger(__name__)
    db = connect(db_name, host=db_host, port=db_port)
    log.info("Connected to MongoDB at %s:%s using database name '%s'" % (db_host, db_port, db_name))
