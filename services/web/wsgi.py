import os, sys
from tmtar import *
from tmtar.project import create_app

app = create_app(True).Instance().app

print('App imported successfully')


@app.route('/health', methods=['GET'])
def health():
    return "Healthy"


@app.route('/init_db', methods=['GET'])
def init_db():
    db = create_app().Instance().init_db()
    return f"Database initialized successfully with {id(db)}"


def start_app():
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    start_app()
