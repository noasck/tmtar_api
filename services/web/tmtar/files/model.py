from ..injectors.app import FlaskApp

db = FlaskApp.Instance().database


class File(db.Model):
    """File Widget responsible for saving filenames"""

    __tablename__ = 'files'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)

    def update(self):
        raise NotImplementedError('Update method is unavailable 4 immutable instance')
