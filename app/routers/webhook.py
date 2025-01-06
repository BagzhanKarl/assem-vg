from flask import Blueprint, request, jsonify
from app.db import User, Messages
from app.utils import add_task, AssemMessage, AssemAI

weebhook_bp = Blueprint('weebhook_bp', __name__)



@weebhook_bp.route('/webhook/whatsapp', methods=['POST'])
def webhook():
    try:
        post_data = request.get_json()
        if not post_data or 'messages' not in post_data:
            return jsonify({'status': False, 'error': 'Invalid payload'}), 400

        data = post_data['messages'][0]
        phone = data.get('from')
        name = data.get('from_name')
        chat_id = data.get('chat_id')

        if not phone or not chat_id:
            return jsonify({'status': False, 'error': 'Phone or Chat ID missing'}), 400

        # Сохраняем пользователя на базу
        user = User(fullname=name, phone=phone, chat_id=chat_id)
        user.save_to_db()
        message = AssemMessage()
        if 'text' in data:
            message_body = data['text'].get('body')
            if message_body:
                message = Messages(
                    user_id=user.id,
                    role='user',
                    content=message_body,
                    tool_call_id=None,
                )
                message.save_to_db()
                context = message.get_context_for_ai(chat_id=chat_id)
                api_key = ''
                ai = AssemAI(api_key=api_key)
                text = ai.generate_answer(context)
                # add_task(chat_id)
                hand = AssemMessage()
                hand.send_text(text, chat_id)
                aitext = Messages(
                    user_id=user.id,
                    role='assistant',
                    content=text,
                    tool_call_id=None,
                )
                aitext.save_to_db()
                return jsonify({'status': True, 'data': 'Thanks guys! We take that!', 'context': context})
        elif 'image' in data:
            ans = ('Спасибо за отправленное изображение! К сожалению, я пока не умею читать содержимое картинок. '
                   'Попробуйте описать текст из изображения словами, и я обязательно помогу вам! 😊')
            response = message.send_text(ans, chat_id)
        elif 'voice' in data:
            ans = ('Спасибо за отправленное голосовое сообщение! Пока я не могу слушать аудиофайлы, но буду рад, '
                   'если вы напишете то же самое текстом. Это поможет мне лучше вам помочь! ')
            response = message.send_text(ans, chat_id)
        else:
            ans = (
                'Я не смог понять отправленное сообщение. Пожалуйста, напишите мне текстом, чтобы мы продолжили общение. '
                'Я здесь, чтобы помочь! ')
            response = message.send_text(ans, chat_id)

        return jsonify({'status': True, 'data': 'Thanks guys! We take that!', 'a': ans})

    except Exception as e:
        return jsonify({'status': False, 'error': str(e)}), 500
