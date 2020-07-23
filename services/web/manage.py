from flask.cli import FlaskGroup
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from project import app, db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
