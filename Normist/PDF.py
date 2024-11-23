from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf(filename, text):
    # Создаем объект canvas для работы с PDF
    c = canvas.Canvas(filename, pagesize=A4)

    # Устанавливаем начальные координаты для текста
    x = 50
    y = 800

    # Добавляем текст в PDF
    c.setFont("Helvetica", 12)
    c.drawString(x, y, text)

    # Сохраняем PDF-файл
    c.save()


if __name__ == "__main__":
    # Текст, который будет добавлен в PDF
    text = "Привет, это пример текста в PDF-файле!"

    # Имя файла для сохранения
    filename = "example.pdf"

    # Создаем PDF-файл
    create_pdf(filename, text)

    print(f"PDF файл '{filename}' успешно создан.")