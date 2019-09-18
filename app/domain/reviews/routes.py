import flask

import app.domain.reviews.crud_service as crud
import app.domain.reviews.rest_validations as rest_validator
import app.utils.errors as errors
import app.utils.json_serializer as json
import app.utils.security as security


def init(app):

    @app.route('/v1/reviews/<string:id_article>', methods=['POST'])
    def create_review(id_article):
        user = security.isValidToken(flask.request.headers.get("Authorization"))
        parameters = json.body_to_dic(flask.request.data)
        parameters.update({'id_article': id_article})
        parameters = rest_validator.validateAddorEditReview(parameters)
        result = crud.add_review(parameters, user["id"])
        return json.dic_to_json(result)

    @app.route('/v1/reviews/<string:id_article>', methods=['DELETE'])
    def delete_review(id_article):
        if flask.request.data:
            parameters = json.body_to_dic(flask.request.data)
            if "id_user" in parameters:
                security.validateAdminRole(flask.request.headers.get("Authorization"))
                return json.dic_to_json(crud.disable_review(id_article, parameters['id_user']))
        user = security.isValidToken(flask.request.headers.get("Authorization"))
        result = crud.disable_review(id_article, user['id'])
        return json.dic_to_json(result)

    @app.route('/v1/reviews/<string:id_article>', methods=['GET'])
    def get_reviews_article(id_article):
        security.isValidToken(flask.request.headers.get("Authorization"))
        result = crud.get_article_reviews(id_article)
        return json.dic_to_json(result)

    @app.errorhandler(Exception)
    def handle_errors(err):
        return errors.handleError(err)
