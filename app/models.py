from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tools = db.relationship('UserSoftware', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class SoftwareTool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    vendor = db.Column(db.String(128))
    official_website = db.Column(db.String(256))
    users = db.relationship('UserSoftware', back_populates='software')

    def __repr__(self):
        return f'<SoftwareTool {self.name}>'

class UserSoftware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    software_id = db.Column(db.Integer, db.ForeignKey('software_tool.id'))
    user = db.relationship('User', back_populates='tools')
    software = db.relationship('SoftwareTool', back_populates='users')

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software_tool.id'))
    version = db.Column(db.String(64))
    release_date = db.Column(db.DateTime)
    raw_notes = db.Column(db.Text)
    summary = db.Column(db.Text)

    def __repr__(self):
        return f'<Update {self.software_id} - {self.version}>'

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sent_date = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Newsletter {self.user_id} - {self.sent_date}>'
