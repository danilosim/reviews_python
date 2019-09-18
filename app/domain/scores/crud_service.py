import datetime

import http.client
import socket

import app.domain.scores.score_schema as schema
import app.utils.config as config
import app.utils.mongo as db
import app.utils.errors as errors
import app.utils.json_serializer as json
import app.gateway.rabbit as rabbit

import memoize

memo_keys = {}
memo = memoize.Memoizer(memo_keys)


def add_score(parameters, id_user):
    """
        @api {post} /v1/scores/<string:id_article> Crear Score
        @apiName Crear Score
        @apiGroup Scores

        @apiUse AuthHeader

        @apiExample {json} Body
            {
                "value": {puntuación del 1 al 10}
            }

        @apiSuccessExample {json} Respuesta
            HTTP/1.1 200 OK
            {
                "_id": "{id del review}",
                "id_article": "{id del artículo}",
                "id_user": "{id del user}",
                "value": {puntuación del 1 al 10},
                "updated": {fecha ultima actualización},
                "created": {fecha creación}
            }

        @apiUse Errors

    """
    get_article(parameters['id_article'])

    score = schema.new_score()

    r = db.score.find_one({'id_user': id_user, 'id_article': parameters['id_article'], 'active': True})
    if r:
        r.update({"active": False, "updated": datetime.datetime.utcnow(), "value": parameters['value']})
        db.score.replace_one({'id_user': id_user, 'id_article': parameters['id_article'], 'active': True}, r)
        del r['active']

        rabbit.send_new_score(parameters['id_article'], calculate_score(parameters['id_article']))

        return r

    score.update(parameters)
    score.update({"id_user": id_user, 'value': parameters['value'], 'id_article': parameters['id_article']})

    schema.validate_schema(score)

    score['_id'] = db.score.insert_one(score).inserted_id
    del score['active']

    rabbit.send_new_score(parameters['id_article'], calculate_score(parameters['id_article']))

    return score


def disable_score(id_article, id_user):
    """
        @api {delete} /v1/scores/<string:id_article> Borrar Score
        @apiName Borrar Score
        @apiGroup Scores

        @apiUse AuthHeader

        @apiSuccessExample {json} Respuesta
            HTTP/1.1 200 OK
            {
                "deleted": true
            }

        @apiUse Errors

    """
    get_article(id_article)

    r = db.score.find_one({'id_user': id_user, 'id_article': id_article, 'active': True})
    if r:
        r.update({"active": False, "updated": datetime.datetime.utcnow()})
        db.score.replace_one({'id_user': id_user, 'id_article': id_article, 'active': True}, r)

        rabbit.send_new_score(id_article, calculate_score(id_article))

        return {"deleted": True}
    else:
        raise errors.InvalidRequest("No existe un score activo para este articulo")


def get_score_article(id_article):
    """
        @api {post} /v1/scores/<string:id_article> Obtener Score
        @apiName Obtener Score
        @apiGroup Scores

        @apiUse AuthHeader

        @apiSuccessExample {json} Respuesta
            HTTP/1.1 200 OK
            {
                "id_article": "{id del artículo}",
                "value": {puntuación del 1 al 10},
            }

        @apiUse Errors

    """

    get_article(id_article)
    score = calculate_score(id_article)

    return {'id_article': id_article, 'value': float("%.2f" % score)}


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


def calculate_score(id_article):
    r = [score for score in db.score.find({'id_article': id_article, 'active': True})]
    if not r:
        raise errors.InvalidRequest("Nadie le ha dado un score a este articulo")

    count = 0
    accum = 0
    for item in r:
        accum += item['value']
        count += 1

    return accum / count
