from flasgger import Swagger

swagger_config = {
    "openapi": "3.0.2",
    "headers": [],
    "components": {
        "securitySchemes": {
          "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
          }
        }
    },
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/docs/swagger.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "title": "Flapisk API Documentation",
    "version": "0.0.1",
    "termsOfService": "",
    "static_url_path": "/static/swagger",
    "swagger_ui": True,
}

swagger = Swagger(
    config=swagger_config,
)
