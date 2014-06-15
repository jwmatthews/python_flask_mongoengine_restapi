import logging
from flask import jsonify, render_template, request

from sampleapp import app
from sampleapp.exceptions import *
from sampleapp.models import *

log = logging.getLogger(__name__)

def log_request_params():
    log.info("request.data = <%s>" % (request.data))
    log.info("request.form = <%s>" % (request.form))
    log.info("request.args = <%s>" % (request.args))
    log.info("request.values = <%s>" % (request.values))
    log.info("request.headers = <%s>" % (request.headers))

@app.route("/", methods=["GET"])
def index():
    items = Item.objects()
    # pagination would be implemented for a real world system
    return render_template("index.html", items=items)

@app.route("/items/", methods=["GET"])
def all():
    items = Item.objects()
    return items.to_json()

@app.route("/items/", methods=["POST"])
def create():
    log_request_params()
    data = request.get_json(force=True)
    item = Item(**data)
    item.save(force_insert=True)
    return item.to_json()

@app.route("/items/<name>/", methods=["GET"])
def read(name):
    items = Item.objects(name=name)
    if not items:
        raise MissingResource("No resource with name: '%s'" % name)
    return items.to_json()

@app.route("/items/<name>/", methods=["PUT"])
def update(name):
    items = Item.objects(name=name)
    if not items:
        raise MissingResource("No resource with name: '%s'" % name)
    log_request_params()
    data = request.get_json(force=True)
    item = items[0]
    for k in data.keys():
        item[k] = data[k]
    item.save()
    items = Item.objects(name=name)    
    return items.to_json()

@app.route("/items/<name>/", methods=["DELETE"])
def delete(name):
    items = Item.objects(name=name)
    if not items:
        raise MissingResource("No resource with name: '%s'" % name)
    item = items[0]
    item.delete()
    return item.to_json()

