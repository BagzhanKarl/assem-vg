from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.db import User, Messages
from app.utils import add_task, AssemMessage, AssemAI

weebhook_bp = Blueprint('weebhook_bp', __name__)


def get_message_content(message):
    """Helper function to process different message types"""
    msg_type = message.get('type')

    if msg_type == 'text':
        return message.get('text', {}).get('body'), None

    type_messages = {
        'voice': 'Пожалуйста, отправьте ваше сообщение в текстовом виде вместо голосового сообщения',
        'image': 'Пожалуйста, отправьте описание изображения в текстовом виде',
        'video': 'Пожалуйста, опишите содержание видео текстом',
        'document': 'Пожалуйста, отправьте содержание документа в текстовом виде'
    }

    return type_messages.get(msg_type, 'Пожалуйста, отправьте сообщение в текстовом виде'), msg_type



@weebhook_bp.route('/hook/messages', methods=['POST'])
def handle_new_messages():
    try:
        messages = request.json.get('messages', [])
        response_data = []

        for message in messages:
            if message.get('from_me'):
                continue

            # Извлекаем данные пользователя
            chat_id = message.get('chat_id')
            phone = message.get('from')
            name = message.get('from_name')

            # Проверяем существует ли пользователь
            user = User.query.filter_by(phone=phone).first()

            if not user:
                # Создаем нового пользователя
                user = User(
                    fullname=name,
                    phone=phone,
                    chat_id=chat_id,

                )
                db.session.add(user)
                db.session.flush()

            # Получаем контент и тип сообщения
            content, msg_type = get_message_content(message)

            # Создаем новое сообщение
            new_message = Messages(
                role='user',
                content=content,
                tool_calls=msg_type,  # Сохраняем тип сообщения, если это не текст
                user_id=user.id,
            )
            db.session.add(new_message)

            context = new_message.get_context_for_ai(chat_id=chat_id)

            api_key = ''
            client = AssemAI(api_key=api_key)
            text = client.generate_answer(context)
            # add_task(chat_id)
            hand = AssemMessage()
            hand.send_text(text, chat_id)

            response_data.append({
                'status': 'success',
                'user_id': user.id,
                'message_id': message.get('id'),
                'message_type': msg_type if msg_type else 'text'
            })

        # Сохраняем все изменения
        db.session.commit()

        return jsonify({
            'status': 'success',
            'data': response_data
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400