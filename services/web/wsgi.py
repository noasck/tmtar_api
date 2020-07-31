import os, sys
from tmtar import *
from tmtar.project import create_app

app = create_app()
if __name__ == "__main__":
    app.Instance().run(host='0.0.0.0', debug=True)