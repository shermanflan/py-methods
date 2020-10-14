

from flask_sqlalchemy import SQLAlchemy

from flask_methods.util.app_config import (ENGINE_OPTS, SESSION_OPTS)


def get_db(app):
    """
    Bind db to Flask

    :param app: the current app
    :return: the database
    """
    return SQLAlchemy(app, session_options=SESSION_OPTS, engine_options=ENGINE_OPTS)