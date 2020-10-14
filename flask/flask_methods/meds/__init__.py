import json

from flask import (request, abort, Blueprint, current_app,
                   Response)
from sqlalchemy import text

from .model import GlobalMedList
from .schema import MedSchema
from flask_methods.util.log_config import root_logger as logger


med_api = Blueprint('pah', __name__, url_prefix='/rx_api/v1')


class StreamArray(list):
    """
    Class to serialize a generator as a list.
    Inspired by:
    https://stackoverflow.com/questions/21663800/python-make-a-list-generator-json-serializable
    """
    def __init__(self, f):
        super().__init__()
        self.gen = f

    def __iter__(self):
        return self.gen()

    def __len__(self):
        return 1


@med_api.before_request
def token_required():
    if 'token' not in request.args \
            or request.args['token'] != current_app.config['APP_SECRET']:
        abort(401, "You are not authorized.")


# Association between a URL and its function handler is a route.
@med_api.route('/med/<int:med_id>', methods=['GET'])
def med(med_id):
    """
    Individual medication.

    :param med_id: variable identifier
    :return: Http Response
    """
    db = current_app.db

    # TODO: Use SQL Expressions instead of ORM - more legible.
    med_1 = db.session.query(GlobalMedList) \
        .filter(text("ID = :id")) \
        .params(id=med_id) \
        .first()

    if not med_1:
        abort(404)  # not found

    payload = MedSchema.dump(med_1, many=False)
    logger.debug(f"Medication: {payload}")

    return payload, 200


@med_api.route('/meds', methods=['GET'])
def meds():
    """
    Multiple medications.

    :return: Http Response
    """
    db = current_app.db
    default_limit = 500
    default_filter = '%'

    if 'limit' in request.args:
        default_limit = int(request.args['limit'])

    if 'name' in request.args:
        default_filter = request.args['name']+'%'

    # TODO: This is an unverified attempt at streaming a response.
    # See: https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/
    def generate():
        med_list = db.session.query(GlobalMedList) \
            .filter(text("NAME LIKE :prefix")) \
            .params(prefix=default_filter) \
            .order_by(GlobalMedList.Id) \
            .limit(default_limit)

        for med in med_list:
            yield MedSchema.dump(med)

    response = Response()
    response.data = json.dumps(StreamArray(generate))
    response.status_code = 200
    response.mimetype = 'application/json'

    return response


