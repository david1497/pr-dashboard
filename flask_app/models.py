from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app import login, db

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    f_name: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=False)
    l_name: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=False)
    username: so.Mapped[str] = so.mapped_column(sa.String(25), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(45), index=True, unique=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(25), index=True, unique=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'<Username: {self.username} | Email: {self.email} | Role: {self.role}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)