from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import asyncio
import orm
from myLogger import logger


def create_pdf(filename, text):
    # Регистрируем шрифт с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    # Создаем объект canvas для работы с PDF
    c = canvas.Canvas(filename, pagesize=A4)

    # Устанавливаем начальные координаты для текста
    x = 50
    y = 800

    # Добавляем текст в PDF
    c.setFont("DejaVuSans", 12)
    c.drawString(x, y, text)

    # Сохраняем PDF-файл
    c.save()


async def cycle():
    while True:
        task = await orm.get_tasks_by_need_pdf()
        if task:
            for report in await orm.get_reports_by_tid(task[0]):
                logger.debug(report)
            # Текст, который будет добавлен в PDF
            text = "Привет, это пример текста в PDF-файле с русскими буквами!"

            # Имя файла для сохранения
            filename = os.path.join('PDFs', f"report{task[0]}.pdf")

            # Создаем PDF-файл
            create_pdf(filename, text)

            logger.info(f"PDF файл '{filename}' успешно создан.")
            await orm.complete_pdf_task(task[0])
        else:
            await asyncio.sleep(5)
            logger.debug("Нет задач для PDF")


def main():
    logger.info("PDF цикл запущен")
    try:
        asyncio.run(cycle())
    except KeyboardInterrupt:
        logger.info("PDF цикл остановлен")


if __name__ == "__main__":
    main()
