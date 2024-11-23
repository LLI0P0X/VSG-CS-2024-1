import flet as ft

def main(page: ft.Page):
    page.title = "Ввод текста"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Создаем три текстовых поля
    text_field1 = ft.TextField(label="Введите текст 1")
    text_field2 = ft.TextField(label="Введите текст 2")
    text_field3 = ft.TextField(label="Введите текст 3")

    # Создаем кнопку отправки
    def button_clicked(e):
        # Здесь можно добавить логику обработки введенных данных
        print(f"Текст 1: {text_field1.value}")
        print(f"Текст 2: {text_field2.value}")
        print(f"Текст 3: {text_field3.value}")
        page.update()

    submit_button = ft.ElevatedButton("Отправить", on_click=button_clicked)

    # Добавляем элементы на страницу
    page.add(
        text_field1,
        text_field2,
        text_field3,
        submit_button
    )

ft.app(target=main)