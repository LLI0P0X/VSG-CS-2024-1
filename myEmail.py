import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import asyncio

import os
from secret import from_email  # Замените на ваш email
from secret import password  # Замените на ваш пароль
import orm
from myLogger import logger


def send_email(subject, body, to_email, attachment_path):
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


async def cycle():
    while True:
        task = await orm.get_task_by_need_send()
        if task:
            for report in await orm.get_reports_by_tid(task[0]):
                logger.debug(report)

            # Отправляем PDF по электронной почте
            filename = os.path.join('PDFs', f"report{task[0]}.pdf")
            subject = "Пример PDF-файла"
            body = "Привет! В этом письме прикреплен PDF-файл с текстом на русском языке."

            to_email = task[7]  # Замените на email получателя

            send_email(subject, body, to_email, filename)

            logger.info(f"PDF файл '{filename}' успешно отправлен на почту {to_email}.")
            await orm.complete_send_task(task[0])
        else:
            await asyncio.sleep(5)
            logger.debug("Нет задач для SMTP")


def main():
    logger.info("SMTP цикл запущен")
    try:
        asyncio.run(cycle())
    except KeyboardInterrupt:
        logger.info("SMTP цикл остановлен")


if __name__ == "__main__":
    main()
