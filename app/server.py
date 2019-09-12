import os.path

import flask
from flask_cors import CORS

import app.domain.reviews.routes as reviewRoutes
# import app.domain.scores.route as scoreRoutes
# import app.gateway.rabbit_service as rabbitService
import app.utils.config as config

class MainApp:
    def __init__(self):
        self.flask_app = flask.Flask(__name__, static_folder='../public')
        CORS(self.flask_app, supports_credentials=True, automatic_options=True)

        # self._generate_api_doc()
        # self._init_routes()
        # self._init_rabbit()
        self._init_reviews()
        # self._init_scores()

    def _generate_api_doc(self):
        os.system("apidoc -i ./ -o ./public")

    def _init_routes(self):
        # Servidor de archivos estáticos de apidoc
        # Por el momento se genera con ../auth/node_modules/.bin/apidoc -i ./ -o public
        @self.flask_app.route('/<path:path>')
        def api_index(path):
            return flask.send_from_directory('../public', path)

        @self.flask_app.route('/')
        def index():
            return flask.send_from_directory('../public', "index.html")

    def _init_rabbit(self):
        rabbitService.init()

    def _init_reviews(self):
        reviewRoutes.init(self.flask_app)

    def _init_scores(self):
        scoreRoutes.init(self.flask_app)

    def get_flask_app(self):
        return self.flask_app

    def start(self):
        self.flask_app.run(port=config.get_server_port())
