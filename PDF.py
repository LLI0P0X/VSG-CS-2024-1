from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import asyncio

from sqlalchemy.sql.base import elements

import orm
from myLogger import logger

pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))


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
        task = await orm.get_task_by_need_pdf()
        if task:
            data = [['IP', 'Протокол', 'Порт', 'CVE', 'Опасность', 'Ссылка на CVE']]
            output_folder = 'PDFs'
            filename = os.path.join(output_folder, f"report{task[0]}.pdf")
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            header_style = styles['Heading1']
            header_style.alignment = 1
            header_style.fontName = 'DejaVuSans'  # Используем шрифт с поддержкой кириллицы
            header = Paragraph(f"Отчет о безопасности по адресам {task[1]}-{task[2]}:", header_style)
            elements.append(header)

            reports = await orm.get_reports_by_tid(task[0])
            if len(reports):
                for report in await orm.get_reports_by_tid(task[0]):
                    logger.debug(report)
                    tid = report[1]
                    data.append([])
                    for item in report[2:]:
                        data[len(data) - 1].append(item)

                # Создаем таблицу
                table = Table(data)
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),  # Используем шрифт с поддержкой кириллицы
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ])
                table.setStyle(style)

                table._argW[0] = 1.3 * inch  # Ширина первого столбца
                table._argW[1] = 0.8 * inch  # Ширина второго столбца
                table._argW[2] = 0.8 * inch  # Ширина третьего столбца
                table._argW[3] = 1.7 * inch  # Ширина четвертого столбца
                table._argW[4] = 0.8 * inch  # Ширина пятого столбца
                table._argW[5] = 2.9 * inch  # Ширина шестого столбца

                elements.append(table)
            else:
                logger.info("Нет отчетов для PDF")
                header = Paragraph(f"Уязвимостей не обнаружено", header_style)
                elements.append(header)

            # Создаем PDF-файл
            doc.build(elements)

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
