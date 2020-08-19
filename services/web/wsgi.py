import os, sys # noqa
from tmtar import * # noqa
from tmtar.project import create_app # noqa
from tmtar.injectors.app import FlaskApp # noqa

is_prod_text = bool(os.getenv('PROD_TEST'))
db_init = bool(os.getenv('DB_INIT'))
app = create_app(is_prod_text).Instance().app


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# @app.route('/init_db', methods=['GET'])
def init_db():
    db = FlaskApp.Instance().init_db()
    return f"Database initialized successfully with {id(db)}"


print('App imported successfully')

if db_init:
    init_db()


@app.route('/health', methods=['GET'])
def health():
    return "Healthy"


def start_app():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    start_app()
