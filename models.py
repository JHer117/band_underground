from sqlalchemy.sql import func
from config import db
import bcrypt

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255)) 
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    
class Bands(db.Model):
    __tablename__ = "bands"
    id = db.Column(db.Integer, primary_key=True)
    band_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))#,nullable=False)
    author = db.relationship("Users", foreign_keys=[author_id], backref="users_bands")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())