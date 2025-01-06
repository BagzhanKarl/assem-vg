from flask import Blueprint, render_template, url_for, request

from app.db import Avatar
from app.utils import AssemAI

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    return render_template('index.html')

@admin_bp.route('/avatars')
def avatars():
    avatars = Avatar.query.all()
    return render_template('avatar.html', avatars=avatars)

@admin_bp.route('/avatars/edit/<int:id>', methods=['GET', 'POST'])
def avatars_edit(id):
    if request.method == 'POST':
        title = request.form['title']
        instruction = request.form['instruction']
        temp = request.form['temp']
        avatar = Avatar.query.get(id)
        avatar.update_data(title=title, instruction=instruction, temp=temp)
        if avatar.hardMode:
            """
            Тут мы должны менять настройки Аватар через API и AssistID
            """
            api_key = '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'

            assist = AssemAI(
                api_key=api_key,
                assistant='asst_sr0IcR2W3q5mzhJO0m8o54fT'
            )
            assist.update_assist_data(name=title, instruction=instruction, temp=float(temp))
            pass
        return render_template('avatar-edit.html', avatar=avatar)
    else:
        avatar = Avatar.query.get(id)
        return render_template('avatar-edit.html', avatar=avatar)
@admin_bp.route('/users')
def users():
    return render_template('users.html')

@admin_bp.route('/payment')
def payment():
    return render_template('payment.html')

@admin_bp.route('/status')
def status():
    return render_template('status.html')

@admin_bp.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')