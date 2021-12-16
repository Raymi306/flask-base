import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    flask_app = Flask(__name__)

    @flask_app.route('/heartbeat')
    def heartbeat():
        """For monitoring purposes"""
        return 'up'

    flask_app.config.from_mapping({
        'SECRET_KEY': 'default_unsafe',
        'SQLALCHEMY_DATABASE_URI': f"sqlite:////{os.path.join(flask_app.instance_path, 'leaderboard.sqlite')}",
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        })

    if test_config is None:
        flask_app.config.from_pyfile('config.py', silent=True) # TODO
    else:
        flask_app.config.update(test_config)

    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass

    import app.models.app_user
    db.init_app(flask_app)
    if test_config is None:
        db.create_all()

    from app.blueprints import blueprints, before_hooks, after_hooks
    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)
    for hook in before_hooks:
        flask_app.before_request(hook)
    for hook in after_hooks:
        flask_app.after_request(hook)

    return flask_app
