from flask  import Blueprint

from app.db import Avatar

start_bp = Blueprint('start', __name__)
@start_bp.route('/')
def index():
    return "Все установлено и работает!"


@start_bp.route('/create/avatar')
def create_avatar():
    avatar = Avatar(
        title='Арлан 2.0',
        temp=1.0,
        instruction='Это проверка текстов',
        hardMode=True,
        assist_id='asst_sr0IcR2W3q5mzhJO0m8o54fT',
    )

    avatar.save_to_db()
    return "True"

@start_bp.route('/avatar/change/<int:id>', methods=['POST'])
def change_avatar(id):
    avatar = Avatar(id=id)
    avatar.install_data()
    avatar.change_active_mod()
    return "True"