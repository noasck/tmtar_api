from ..injectors.app import FlaskApp

app = FlaskApp.Instance().app


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response