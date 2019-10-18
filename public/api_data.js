define({ "api": [
  {
    "type": "fanout",
    "url": "auth/logout",
    "title": "Logout",
    "group": "RabbitMQ_GET",
    "description": "<p>Escucha eventos de logout provenientes de Auth para borrar tokens del cache.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"article-exist\",\n  \"message\" : \"tokenId\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "app/gateway/rabbit.py",
    "groupTitle": "RabbitMQ_GET",
    "name": "FanoutAuthLogout"
  },
  {
    "type": "fanout",
    "url": "score/new_score",
    "title": "Nuevo Score",
    "group": "RabbitMQ_POST",
    "description": "<p>Enviá mensajes de nuevo score</p>",
    "success": {
      "examples": [
        {
          "title": "Mensaje",
          "content": "{\n  \"type\": \"new_score\",\n  \"message\" : {\n      \"id_article\": \"{id del articulo}\",\n      \"score\": {score promedio del articulo}\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/gateway/rabbit.py",
    "groupTitle": "RabbitMQ_POST",
    "name": "FanoutScoreNew_score"
  },
  {
    "type": "delete",
    "url": "/v1/reviews/<string:id_article>",
    "title": "Borrar Review",
    "name": "Borrar_Review",
    "group": "Reviews",
    "description": "<p>Le permite a un usuario borrar su propia review de un artículo. Si el usuario es admin, puede mandar el id de otro usuario en el body para borrar la review de dicho usuario</p>",
    "examples": [
      {
        "title": "Body",
        "content": "{\n    \"id_user\": \"{id del user del cual se quiere borrar una review en caso de ser admin}\"\n}",
        "type": "json"
      },
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n{\n    \"deleted\": true\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "403 Forbidden",
          "content": "HTTP/1.1 401 Forbidden\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/reviews/review_service.py",
    "groupTitle": "Reviews"
  },
  {
    "type": "post",
    "url": "/v1/reviews/<string:id_article>",
    "title": "Crear Review",
    "name": "Crear_Review",
    "group": "Reviews",
    "examples": [
      {
        "title": "Body",
        "content": "{\n    \"title\": \"{título del review}\",\n    \"description\": \"{comentario sobre el artículo}\"\n}",
        "type": "json"
      },
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n{\n    \"_id\": \"{id del review}\",\n    \"id_article\": \"{id del artículo}\",\n    \"id_user\": \"{id del user}\",\n    \"title\": \"{título del review}\",\n    \"description\": \"{comentario del review}\",\n    \"updated\": {fecha ultima actualización},\n    \"created\": {fecha creación}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/reviews/review_service.py",
    "groupTitle": "Reviews",
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/v1/reviews/<string:id_article>",
    "title": "Ver Reviews de un Artículo",
    "name": "Ver_Reviews_de_un_Art_culo",
    "group": "Reviews",
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n[\n    {\n        \"_id\": \"{id del review}\",\n        \"id_article\": \"{id del artículo}\",\n        \"id_user\": \"{id del user}\",\n        \"title\": \"{título del review}\",\n        \"description\": \"{comentario del review}\",\n        \"updated\": {fecha ultima actualización},\n        \"created\": {fecha creación}\n    },...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/reviews/review_service.py",
    "groupTitle": "Reviews",
    "examples": [
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/v1/scores/<string:id_article>",
    "title": "Borrar Score",
    "name": "Borrar_Score",
    "group": "Scores",
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n{\n    \"deleted\": true\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/scores/score_service.py",
    "groupTitle": "Scores",
    "examples": [
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/v1/scores/<string:id_article>",
    "title": "Crear Score",
    "name": "Crear_Score",
    "group": "Scores",
    "examples": [
      {
        "title": "Body",
        "content": "{\n    \"value\": {puntuación del 1 al 10}\n}",
        "type": "json"
      },
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n{\n    \"_id\": \"{id del review}\",\n    \"id_article\": \"{id del artículo}\",\n    \"id_user\": \"{id del user}\",\n    \"value\": {puntuación del 1 al 10},\n    \"updated\": {fecha ultima actualización},\n    \"created\": {fecha creación}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/scores/score_service.py",
    "groupTitle": "Scores",
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/v1/scores/<string:id_article>",
    "title": "Obtener Score",
    "name": "Obtener_Score",
    "group": "Scores",
    "success": {
      "examples": [
        {
          "title": "Respuesta",
          "content": "HTTP/1.1 200 OK\n{\n    \"id_article\": \"{id del artículo}\",\n    \"value\": {puntuación del 1 al 10},\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/domain/scores/score_service.py",
    "groupTitle": "Scores",
    "examples": [
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  }
] });
