from flask import Flask
from flask_script import Manager
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
        db.session.remove()
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
                email=str('denter425@gmail.com'),
                location_id=1,
                admin_location_id=1,
            )
            u2: User = User(
                id=5,
                email=str('jjok730@gmail.com'),
                location_id=1,
                admin_location_id=1,
            )

            root_location = Location(id=1, root=None, name='root')

            db.session.add(u1)
            db.session.add(u2)
            db.session.add(root_location)
            db.session.commit()

            for user in User.query.all():
                app.logger.info(f'Successfully seeded {user.email} root user.')
        else:
            app.logger.info('Skipped database seeding.')

    @classmethod
    def add_cli(cls, app: Flask, db: SQLAlchemy, manager: Manager):
        """
        Register CLI commands for db manipulation.

        :param manager: Flask-Script manager.
        :type manager: Manager
        :param app: main Flask app.
        :type app: Flask
        :param db: db connection instance.
        :type db: SQLAlchemy
        """
        @manager.command
        def set_up():
            """Create all ab tables and seed values."""
            DatabaseSetup.set_up_db(app, db)
            DatabaseSetup.seed_db(app, db)

        @manager.command
        def tear_down():
            """Drop all ab tables."""
            DatabaseSetup.tear_down_db(app, db)

        @manager.command
        def seed_db():
            """Seed necessary records in."""
            DatabaseSetup.seed_db(app, db)
