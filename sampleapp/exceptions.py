import logging
from flask import jsonify
from mongoengine.errors import OperationError, NotUniqueError

from sampleapp import app

log = logging.getLogger(__name__)

class ApiException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv    

class InvalidUsage(ApiException):
    status_code = 400

class MissingResource(ApiException):
    status_code = 404


###
# Order is important for registering the error handlers
# Order as:  Most Specific exception class to least specific
###
@app.errorhandler(ApiException)
def handle_api_exception(error):
    log.error(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(NotUniqueError)
def handle_mongoengine_not_unique_error(error):
    log.error(error)
    status_code = 409
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(OperationError)
def handle_mongoengine_operation_error(error):
    log.error(error)
    status_code = 400
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(BaseException)
def handle_base_exception(error):
    log.error(error)
    status_code = 500
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(AssertionError)
def handle_assertion_error(error):
    log.error(error)
    status_code = 400
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response
