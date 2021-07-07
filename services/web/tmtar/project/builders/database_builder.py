from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class DatabaseSetup(object):
    """Database administration logic."""

    @classmethod
    def set_up_db(cls, app: Flask, db: SQLAlchemy):
        """
        Create all db tables.

        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """
        app.logger.info('Creating db tables...')
        db.create_all()
        db.session.commit()

    @classmethod
    def tear_down_db(cls, app: Flask, db: SQLAlchemy):
        """
        Delete all db tables.

        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """
        app.logger.info('Removing db tables...')
        db.session.remove()
        db.session.execute('drop table if exists locations cascade;')
        db.session.commit()
        db.drop_all()
        db.session.commit()

    @classmethod
    def seed_db(cls, app: Flask, db: SQLAlchemy) -> None:
        """
        Seed database with necessary records.

        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """
        from ...locations.service import Location
        from ...users.model import User
        if Location.query.get(1) is None:
            u1: User = User(
                id=4,
                identity='google-oauth2|112161506929078504169',
                location_id=1,
                admin_location_id=1,
            )
            u2: User = User(
                id=5,
                identity='auth0|609fd1ff3872bb0068e63812',
                location_id=1,
                admin_location_id=1,
            )

            root_location = Location(id=1, root=None, name='root')

            db.session.add(u1)
            db.session.add(u2)
            db.session.add(root_location)
            db.session.commit()

            for user in User.query.all():
                app.logger.info(f'Successfully seeded {user.identity} root user.')
        else:
            app.logger.info('Skipped database seeding.')
