from flask_restful import Api
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException


class GolfApi(Api):
    # https://stackoverflow.com/questions/41149409/flask-restful-custom-error-handling
    def handle_error(self, err):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        print(err)    # log every exception raised in the application
        # Handle HTTPExceptions
        if isinstance(err, HTTPException):
            return jsonify({'message': getattr(err, 'description', HTTP_STATUS_CODES.get(err.code, ''))}), err.code
        # If msg attribute is not set,
        # consider it as Python core exception and
        # hide sensitive error info from end user
        if not getattr(err, 'message', None):
            # Handle application specific custom exceptions
            error = self.errors[type(err).__name__]
            return jsonify({"message": error["message"]}), error["status"]

        return jsonify(**err.kwargs), err.http_status_code
