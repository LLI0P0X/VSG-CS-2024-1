import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(subject, body, to_email, attachment_path):
    from secret import from_email  # Замените на ваш email
    from secret import password  # Замените на ваш пароль

    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Добавляем тело письма
    msg.attach(MIMEText(body, 'plain'))

    # Открываем файл в бинарном режиме
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Кодируем файл в строку
    encoders.encode_base64(part)

    # Добавляем заголовок к вложению
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {os.path.basename(attachment_path)}',
    )

    # Добавляем вложение к сообщению
    msg.attach(part)

    # Отправляем письмо
    with smtplib.SMTP('smtp.mail.ru', 587) as server:  # Замените на ваш SMTP сервер и порт
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())


if __name__ == '__main__':
    # Отправляем PDF по электронной почте
    subject = "Пример PDF-файла"
    body = "Привет! В этом письме прикреплен PDF-файл с текстом на русском языке."
    emails = ["normist@yandex.ru"]  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Здесь добавлять емаилы
    for email in emails:
        to_email = email  # Замените на email получателя

        send_email(subject, body, to_email, filename)

        print(f"PDF файл '{filename}' успешно отправлен на почту {to_email}.")
