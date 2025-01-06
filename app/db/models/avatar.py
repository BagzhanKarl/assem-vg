from app.db import db



class Avatar(db.Model):
    __tablename__ = 'avatar'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    hardMode = db.Column(db.Boolean, nullable=False)
    assist_id = db.Column(db.String(150), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False)

    def __init__(self, title=None, temp=None, instruction=None, hardMode=False, assist_id=None, is_active=False, id=None):
        self.title = title
        self.temp = temp
        self.instruction = instruction
        self.hardMode = hardMode
        self.assist_id = assist_id
        self.is_active = is_active
        self.id = id

    def install_data(self):
        installer = Avatar.query.get(self.id)
        self.title = installer.title
        self.temp = installer.temp
        self.instruction = installer.instruction
        self.hardMode = installer.hardMode
        self.assist_id = installer.assist_id
        self.is_active = installer.is_active
        self.id = installer.id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return True

    def change_active_mod(self):
        all = Avatar.query.all()
        for a in all:
            a.is_active = False
        change = Avatar.query.filter_by(id=self.id).first()
        change.is_active = True
        db.session.commit()
        return True

    def update_data(self, **kwargs):
        for key, value in kwargs.items():
            # Проверяем, есть ли у объекта такое свойство
            if hasattr(self, key):
                setattr(self, key, value)  # Устанавливаем новое значение

            # Сохраняем изменения в базе данных
        db.session.commit()
        return True

