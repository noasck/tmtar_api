from flask import Flask


def register_cors(app: Flask):
    """
    Implements CORS headers policy  middleware.
    @param app: main Flask object
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers',
                             'Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response
