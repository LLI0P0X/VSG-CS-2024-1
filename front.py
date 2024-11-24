import flet as ft
import re
import ipaddress
import sqlite3
import threading
import asyncio
import datetime

from orm import add_task

def main(page: ft.Page):
    page.title = "IP Address Input"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def parse_timedelta(time_str):
        # Регулярное выражение для извлечения числа и единицы измерения
        pattern = r'(\d+)([smhdw])'
        match = re.match(pattern, time_str)

        if not match:
            raise ValueError("Неверный формат строки")

        value = int(match.group(1))
        unit = match.group(2)

        # Создание timedelta на основе единицы измерения
        if unit == 's':
            return datetime.timedelta(seconds=value)
        elif unit == 'm':
            return datetime.timedelta(minutes=value)
        elif unit == 'h':
            return datetime.timedelta(hours=value)
        elif unit == 'd':
            return datetime.timedelta(days=value)
        elif unit == 'w':
            return datetime.timedelta(weeks=value)
        else:
            raise ValueError("Неизвестная единица измерения")

    def validate_ip_address(ip_text):
        try:
            if '/' in ip_text:
                network = ipaddress.IPv4Network(ip_text, strict=False)
                return True
            elif '-' in ip_text:
                start, end = ip_text.split('-')
                ipaddress.IPv4Address(start.strip())
                ipaddress.IPv4Address(end.strip())
                return True
            else:
                ipaddress.IPv4Address(ip_text)
                return True
        except ValueError:
            return False

    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def validate_port(port):
        try:
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return True
            else:
                return False
        except ValueError:
            return False

    def start_work(e):
        ip_text = ip_input.value.strip()
        email = email_input.value.strip()
        date = date_input.value if use_date.value else None
        if date != None:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        periodicity = periodicity_input.value if use_periodicity.value else None
        if periodicity != None:
            periodicity = parse_timedelta(periodicity)
        port = port_input.value.strip() if use_port.value else None

        if not ip_text:
            ip_input.error_text = "IP address is required"
            page.update()
            return

        if not validate_ip_address(ip_text):
            ip_input.error_text = "Invalid IP address"
            page.update()
            return

        if send_to_email.value and not validate_email(email):
            email_input.error_text = "Invalid email address"
            page.update()
            return

        if use_port.value and not validate_port(port):
            port_input.error_text = "Invalid port number"
            page.update()
            return

        ip_input.error_text = None
        email_input.error_text = None
        port_input.error_text = None

        # Добавление IP-адреса в базу данных
        if '/' in ip_text:
            network = ipaddress.IPv4Network(ip_text, strict=False)
            start_ip = str(network.network_address)
            end_ip = str(network.broadcast_address)
            asyncio.run(add_task(start_ip, end_ip, port, date, periodicity, email))
        elif '-' in ip_text:
            start, end = ip_text.split('-')
            asyncio.run(add_task(start.strip(), end.strip(), port, date, periodicity, email))
        else:
            asyncio.run(add_task(ip_text, ip_text, port, date, periodicity, email))

        ip_list.controls.clear()
        message_success = f'{ip_text} добавлен в работу'
        ip_list.controls.append(ft.Text(message_success))
        ip_input.value = ""
        page.update()

    ip_input = ft.TextField(label="Enter IP Address (single, range, or CIDR)", width=400)
    add_button = ft.ElevatedButton("Запустить работу", on_click=start_work)
    ip_list = ft.Column()
    send_to_email = ft.Checkbox(label="Send to email", on_change=lambda e: page.update())
    email_input = ft.TextField(label="Enter email", width=400, visible=False)

    use_date = ft.Checkbox(label="Use date", on_change=lambda e: page.update())
    date_input = ft.TextField(label="Enter date (YYYY-MM-DD)", width=400, visible=False)

    use_periodicity = ft.Checkbox(label="Use periodicity", on_change=lambda e: page.update())
    periodicity_input = ft.TextField(label="Enter periodicity (e.g., 1d, 1w)", width=400, visible=False)

    use_port = ft.Checkbox(label="Use port", on_change=lambda e: page.update())
    port_input = ft.TextField(label="Enter port", width=400, visible=False)

    def send_to_email_changed(e):
        if send_to_email.value:
            email_input.visible = True
        else:
            email_input.visible = False
        page.update()

    def use_date_changed(e):
        if use_date.value:
            date_input.visible = True
        else:
            date_input.visible = False
        page.update()

    def use_periodicity_changed(e):
        if use_periodicity.value:
            periodicity_input.visible = True
        else:
            periodicity_input.visible = False
        page.update()

    def use_port_changed(e):
        if use_port.value:
            port_input.visible = True
        else:
            port_input.visible = False
        page.update()

    send_to_email.on_change = send_to_email_changed
    use_date.on_change = use_date_changed
    use_periodicity.on_change = use_periodicity_changed
    use_port.on_change = use_port_changed

    input_section = ft.Column(
        [
            ft.Row(
                [ip_input, port_input, use_port],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [ip_list],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [send_to_email, email_input],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [use_date, date_input],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [use_periodicity, periodicity_input],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    output_section = ft.Column(
        [
            ft.Text("Output will be displayed here after submission.")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        input_section,
        ft.Row(
            [add_button],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        output_section
    )

ft.app(target=main)