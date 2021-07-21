from ..project.injector import Injector

db = Injector.db


class File(db.Model):  # noqa: WPS110
    """File Widget responsible for saving filenames."""

    __tablename__ = 'files'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String, nullable=False, unique=True)

    # Relations

    events = db.relationship(
        'Event',
        back_populates='image_file',
        foreign_keys='Event.image_file_name',
        passive_deletes='all',
        lazy='noload',
    )

    def update(self):
        """Update file instance."""
        raise NotImplementedError(
            'Update method is unavailable for immutable instance.',
        )
