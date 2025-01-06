from app.db import db


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text, nullable=True)
    tool_calls = db.Column(db.Text, nullable=True)
    tool_call_id = db.Column(db.String(50), nullable=True)
    refusal = db.Column(db.Boolean, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, user_id, role='user', content=None, tool_calls=None, tool_call_id=None, refusal=False):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.refusal = refusal
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving dialogue: {e}")
            return False

    def get_context_for_ai(self, chat_id):

        context = [
            {
                'role': 'user',
                'content': f'Привет, мой ChatID: {chat_id}'
            }
        ]
        messages = Messages.query.filter_by(user_id=self.user_id).all()

        for message in messages:
            if message.tool_call_id or message.tool_calls:
                pass
            else:
                context.append({
                    'role': message.role,
                    'content': message.content,
                })
        return context