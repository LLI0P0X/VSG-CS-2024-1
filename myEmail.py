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


def send_email(subject, body, to_email, attachment_path=None):
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
    if attachment_path:
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

            # Отправляем PDF по электронной почте
            filename = os.path.join('PDFs', f"report{task[0]}.pdf")
            subject = f"Отчет безопасности по задаче {task[0]}"

            reports = await orm.get_reports_by_tid(task[0])

            if len(reports) == 0:
                body = f"Уязвимостей по адресам {task[1]}-{task[2]} не найдено."

            else:
                body = f"Уязвимости по адресам {task[1]}-{task[2]}: \n"
                for report in reports:
                    body += f"\nip: {report[2]}\n"
                    body += f"Протокол: {report[3]}\n"
                    body += f"Порт: {report[4]}\n"
                    body += f"Код уязвимости: {report[5]}\n"
                    body += f"Опасность: {report[6]}\n"
                    body += f"Подробности: {report[7]}\n"

            to_email = task[7]  # Замените на email получателя
            if f'report{task[0]}.pdf' in os.listdir('PDFs'):
                send_email(subject, body, to_email, filename)
                logger.info(f"PDF файл '{filename}' успешно отправлен на почту {to_email}.")
            else:
                send_email(subject, body, to_email)
                logger.info('Отчет успешно отправлен на почту {to_email}.')
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
