

from flask import Flask, jsonify

from flask_methods.meds import med_api
from flask_methods.util.app_config import APP_CONFIG
from flask_methods.util.db_config import get_db


def create_app():

    app = Flask(__name__)
    app.config.from_mapping(APP_CONFIG)
    app.db = get_db(app)
    app.register_blueprint(med_api)

    @app.route("/")
    def index():
        return "This is a traditional API to tasty tacos."

    @app.route("/heartbeat")
    def heartbeat():
        return jsonify({"status": "Tacos online."}), 200

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(error=f"{e}"), 401

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error=f"{e}"), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(error=f"{e}"), 500

    return app
