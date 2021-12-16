from app import db


UUID_LEN = 36
ARGON2_LEN = 32

class User(db.Model):
    """
    An app user can:
        login
        C.R.U.D games
        C.R.U.D tables
    """
    uuid = db.Column(db.LargeBinary(UUID_LEN), primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False) # index
    hash = db.Column(db.LargeBinary(ARGON2_LEN), unique=True, nullable=False)
    login_counter = db.Column(db.Integer, nullable=False, default=0)
