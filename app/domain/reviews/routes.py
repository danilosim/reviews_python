# import flask
#
# import app.domain.articles.crud_service as crud
# import app.domain.articles.find_service as find
# import app.domain.articles.rest_validations as restValidator
# import app.utils.errors as errors
# import app.utils.json_serializer as json
# import app.utils.security as security

def init(app):

    @app.route('/v1/reviews')
    def hello_world():
        return 'Hola'
