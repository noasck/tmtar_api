import os, sys # noqa
from tmtar import * # noqa
from tmtar.project import create_app # noqa
from tmtar.injectors.app import FlaskApp # noqa

is_db_init = bool(os.getenv('DB_INIT'))
app = create_app().Instance().app

app.logger.info('App imported successfully')


@app.route('/health', methods=['GET'])
def health():
    return "Healthy"


def start_app():
    from tmtar.commands.cors_headers import after_request  # noqa
    from tmtar.commands.seed_db import seed_db  # noqa
    if is_db_init:
        db = FlaskApp.Instance().init_db()
        app.logger.info(f"Database initialized successfully with {id(db)}")
    for res, email in seed_db(['denter425@gmail.com', 'jjok730@gmail.com']):
        app.logger.info(f"Successfully seeded {res} root user", email)
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    start_app()
