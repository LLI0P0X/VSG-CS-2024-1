from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf(filename, text):
    # Регистрируем шрифт с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))

    # Создаем объект canvas для работы с PDF
    c = canvas.Canvas(filename, pagesize=A4)

    # Устанавливаем начальные координаты для текста
    x = 50
    y = 800

    # Добавляем текст в PDF
    c.setFont("TimesNewRoman", 12)
    c.drawString(x, y, text)

    # Сохраняем PDF-файл
    c.save()


if __name__ == "__main__":
    # Текст, который будет добавлен в PDF
    text = "Привет, это пример текста в PDF-файле с русскими буквами!"

    # Имя файла для сохранения
    filename = "example_russian.pdf"

    # Создаем PDF-файл
    create_pdf(filename, text)

    print(f"PDF файл '{filename}' успешно создан.")