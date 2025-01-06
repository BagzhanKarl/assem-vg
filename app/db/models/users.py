from datetime import datetime
from app.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    chat_id = db.Column(db.String(80), nullable=False)
    branch = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, fullname=None, phone=None, chat_id=None, branch=None, created_at=None, updated_at=None, id=None):
        self.id = id
        self.fullname = fullname
        self.phone = phone
        self.chat_id = chat_id
        self.branch = branch
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def save_to_db(self):
        existing_user = User.query.filter_by(chat_id=self.chat_id).first()
        if existing_user:
            print(f"User with chat_id {self.chat_id} already exists.")
            self.id=existing_user.id
            return False

        if not self.id:
            db.session.add(self)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to DB: {e}")
            return False

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def update_user_by_id(cls, id, **kwargs):
        user = cls.query.filter_by(id=id).first()
        if not user:
            return False

        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return False

# Example usage:
# user = User(fullname="John Doe", phone="123456789", chat_id="chat123")
# user.save_to_db()
# User.update_user_by_id(1, fullname="Jane Doe", branch="New Branch")
