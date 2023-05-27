from django.core.signing import Signer
from online_service.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    sign = signer.sign(user.username)
    subject_text = f'Активация пользователя {user.username}'
    body_text = f'''Уважаемый пользователь {user.username}!
                   Вы зарегистрировались на сайте "Доска объявлений".
                   Вам необходимо выполнить активацию, чтобы подтвердить свою личность.
                   Для этого пройдите, пожалуйста, по ссылке
                   {host}/{sign}
                   До свидания!
                   С уважением, администрация сайта "Доска объявлений".'''
    user.email_user(subject_text, body_text)