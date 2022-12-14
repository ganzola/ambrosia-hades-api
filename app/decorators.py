from functools import wraps
from http import HTTPStatus

from flask import jsonify
from marshmallow import ValidationError

from app.exceptions.exceptions import *
from app.log import logger
from app.utils.constants import *


def error_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as ve:
            logger.error(f"{ve.__class__.__name__}: {ve}")
            return (
                jsonify({ERROR_RESPONSE: f"Invalid JSON format ({ve})"}),
                HTTPStatus.BAD_REQUEST,
            )
        except ResourceNotFoundException as rnfe:
            logger.error(f"{rnfe.__class__.__name__}")
            return (
                jsonify({ERROR_RESPONSE: f"{rnfe.resource} ({rnfe.resource_id}) not found"}),
                HTTPStatus.NOT_FOUND,
            )
        except ResourceAlreadyExistsException as raee:
            logger.error(f"{raee.__class__.__name__}")
            return (
                jsonify({ERROR_RESPONSE: f"{raee.resource} ({raee.resource_id}) already exists"}),
                HTTPStatus.CONFLICT,
            )

    return wrapper
