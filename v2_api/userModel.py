import re
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Clearance(db.Model):
    """The model that handles the permissions
    """
    __tablename__ = 'clearance'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    clearance_level = db.Column(db.Integer)
    default_clearance_level = db.Column(db.Boolean, default=True)
    users = db.relationship('User', backref='clearance', lazy='dynamic')

    @staticmethod
    def add_clearances():
        """Add the user clearances
        """
        clearances = {
            'guest': 0,
            'customer': 1,
            'caterer': 2,
            '4fr0c0d3': 3
        }

        default_clearance = 'customer'

            for clearance in clearances:
                user_clearance = Clearance.query.filter_by(
                    name=clearance).first()
                    if user_clearance is None:
                        clearance = Clearance(
                            name=clearance,
                            clearance_level=clearances[clearance],
                            default_clearance_level=(clearance == default_clearance))
                        db.session.add(clearance)
                    db.session.commit()

    def __str__(self):
        """Outputting more user-friendly information
        """
        return self.name

    def __repr__(self):
        return 'Clearance {}'.format(self.name)


class User(db.Model):
    """The model that handles the users 
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    clearance_id = db.Column(db.Integer, db.Foreign('clearance.id'))

    def data_validation(self):
        """Data validation methods
        """
        errors = []
        data_is_valid = True

        if self.email:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email) == None:
                data_is_valid = False
                errors.append('Invalid email')
        if self.username:
            temp_username = self.username.split()
            if len(temp_username) == 0:
                data_is_valid = False
                errors.append('Invalid username')

        return data_is_valid, errors

        @password.setter
        def password(self, password):
            """Ensure password is automatically hashed before storage
            """
            self.password_hash = generate_password_hash(password)

        def verify_password(self, password):
            """Check hash value against hash in storage
            """
            return check_password_hash(self.password_hash, password)

        def access_level(self, level):
            """Return True if user is allowed
            """
            return self.clearance.clearance_level >= level

        def save(self):
            """Save and commit user to storage
            """
            db.session.add(self)
            db.session.commit()

        def make_token(self):
            """Create an auth token
            """
            return create_access_token(identity=self.username)
