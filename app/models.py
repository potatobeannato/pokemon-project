from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data['email']
        self.icon = data['icon']
        self.password = self.hash_password(data['password'])

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user passsword to the password provided in the login form
    def check_password_hash(self, login_password):
        return check_password_hash(self.password, login_password)

    # save the user to the database
    def save(self):
        db.session.add(self)  # add the user to the db session
        db.session.commit()  # save everything in the session to the database

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/adventurer/{self.icon}.svg'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    # SELECT * FROM user WHERE id =???
