from uuid import uuid4

from app import db


UUID_LEN = 16


class User(db.Model):
    uuid = db.Column(db.LargeBinary(UUID_LEN), primary_key=True, default=lambda: uuid4().bytes)
    email = db.Column(db.String(254), unique=True, nullable=False) # index
    hash = db.Column(db.String(254), unique=True, nullable=False)
    login_counter = db.Column(db.Integer, nullable=False, default=0)

    def __str__(self):
            return str((self.uuid.hex(), self.email, self.login_counter))

    def __repr__(self):
            return str(self.uuid.hex())
