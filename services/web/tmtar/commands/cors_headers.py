from ..injectors.app import FlaskApp

app = FlaskApp.Instance().app


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Origin, X-Requested-With, Content-Type, Accept, Authorization')
    return response
