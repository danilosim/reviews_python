import datetime

import bson.objectid as bson
import http.client
import socket

import app.domain.reviews.review_schema as schema
import app.utils.config as config
import app.utils.errors as error
import app.utils.mongo as db
import app.utils.errors as errors
import app.utils.json_serializer as json
import memoize

memo_keys = {}
memo = memoize.Memoizer(memo_keys)


def add_review(params, id_user):
    """
    @api {post} /v1/reviews/<string:id_article> Crear Review
    @apiName Crear Review
    @apiGroup Reviews

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "title": "{título del review}",
            "description": "{comentario sobre el artículo}"
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "_id": "{id del review}",
            "id_article": "{id del artículo}",
            "id_user": "{id del user}",
            "title": "{título del review}",
            "description": "{comentario del review}",
            "updated": {fecha ultima actualización},
            "created": {fecha creación}
        }

    @apiUse Errors

    """

    get_article(params['id_article'])

    review = schema.new_review()

    r = db.review.find_one({'id_user': id_user, 'id_article': params['id_article'], 'active': True})
    if r:
        r.update({"active": False, "updated": datetime.datetime.utcnow()})
        db.review.replace_one({'id_user': id_user, 'id_article': params['id_article'], 'active': True}, r)

    review.update(params)
    review.update({"id_user": id_user})

    schema.validate_schema(review)

    review['_id'] = db.review.insert_one(review).inserted_id
    del review['active']

    return review


@memo(max_age=30)
def get_article(id_article):
    conn = http.client.HTTPConnection(
        socket.gethostbyname(config.get_catalog_server_url()),
        config.get_catalog_server_port(),
    )

    try:
        conn.request("GET", "/v1/articles/{}".format(id_article), {})
        response = conn.getresponse()
        if response.status != 200 or (not json.body_to_dic(response.read().decode('utf-8'))['enabled']):
            raise errors.InvalidArgument('id_article', 'Invalido')
        return json.dic_to_json(response.read().decode('utf-8'))
    except Exception:
        raise Exception


def disable_review(id_article, id_user):

    """
    @api {delete} /v1/reviews/<string:id_article> Borrar Review
    @apiName Borrar Review
    @apiGroup Reviews

    @apiDescription Le permite a un usuario borrar su propia review de un artículo. Si el usuario es admin, puede mandar el id de otro usuario en el body para borrar la review de dicho usuario

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "id_user": "{id del user del cual se quiere borrar una review en caso de ser admin}"
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "deleted": true
        }

    @apiUse Errors

    @apiErrorExample 403 Forbidden
            HTTP/1.1 401 Forbidden
            {
                "error" : "{Motivo del error}"
            }

    """

    get_article(id_article)

    result = db.review.find_one({"id_article": id_article, "id_user": id_user, "active": True})
    if not result:
        raise error.InvalidRequest("No hay reviews activas para este producto")
    result["active"] = False
    result["updated"] = datetime.datetime.utcnow()

    schema.validate_schema(result)

    id_review = result['_id']
    del result['_id']
    r = db.review.replace_one({'_id': bson.ObjectId(id_review)}, result)

    return {"deleted": True}


def get_article_reviews(id_article):

    """
        @api {get} /v1/reviews/<string:id_article> Ver Reviews de un Artículo
        @apiName Ver Reviews de un Artículo
        @apiGroup Reviews

        @apiUse AuthHeader

        @apiSuccessExample {json} Respuesta
            HTTP/1.1 200 OK
            [
                {
                    "_id": "{id del review}",
                    "id_article": "{id del artículo}",
                    "id_user": "{id del user}",
                    "title": "{título del review}",
                    "description": "{comentario del review}",
                    "updated": {fecha ultima actualización},
                    "created": {fecha creación}
                },...
            ]

        @apiUse Errors

        """

    get_article(id_article)

    result = [article for article in db.review.find({"id_article": id_article, 'active': True})]
    if not result:
        raise error.InvalidRequest("No hay reviews activas para este producto")

    for f in result:
        del f['active']

    return result

