from flask import make_response


class APIResponse:
    @staticmethod
    def success_200(data):
        response = {
            'error': False,
            'data': data
        }
        return make_response(response, 200)

    @staticmethod
    def success_201(data):
        response = {
            'error': False,
            'data': data
        }
        return make_response(response, 201)

    @staticmethod
    def success_204(data):
        response = {
            'error': False,
            'data': data
        }
        return make_response(response, 204)

    @staticmethod
    def error_400(error=None):
        response = {
            'error': True,
            'message': 'Bad request' if error is None else error
        }
        return make_response(response, 400)

    @staticmethod
    def error_401(error=None):
        response = {
            'error': True,
            'message': 'Unauthorized' if error is None else error
        }
        return make_response(response, 401)

    @staticmethod
    def error_403(error=None):
        response = {
            'error': True,
            'message': 'Forbidden' if error is None else error
        }
        return make_response(response, 403)

    @staticmethod
    def error_404(error=None):
        response = {
            'error': True,
            'message': 'Entity not exist' if error is None else error
        }
        return make_response(response, 404)

    @staticmethod
    def error_409(error=None):
        response = {
            'error': True,
            'message': 'Conflict' if error is None else error
        }
        return make_response(response, 409)

    @staticmethod
    def error_500(error=None):
        response = {
            'error': True,
            'message': 'Internal server error' if error is None else error
        }
        return make_response(response, 500)
