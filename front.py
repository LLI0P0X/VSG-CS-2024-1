import flet as ft
import re
import ipaddress
import sqlite3
import threading
import asyncio
from orm import add_task

# Локальное хранилище потока для соединения с базой данных
db_connection = threading.local()

def get_db_connection():
    if not hasattr(db_connection, 'conn'):
        db_connection.conn = sqlite3.connect('Normist/ip_addresses.db')
        db_connection.cur = db_connection.conn.cursor()
        db_connection.conn.commit()
    return db_connection.conn, db_connection.cur

def main(page: ft.Page):
    page.title = "IP Address Input"
    page.vertical_alignment = ft.MainAxisAlignment.START

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

    def start_work(e):
        ip_text = ip_input.value.strip()
        email = email_input.value.strip()

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

        ip_input.error_text = None
        email_input.error_text = None

        # Добавление IP-адреса в базу данных
        conn, cur = get_db_connection()
        if '/' in ip_text:
            network = ipaddress.IPv4Network(ip_text, strict=False)
            start_ip = str(network.network_address)
            end_ip = str(network.broadcast_address)
            asyncio.run(add_task(start_ip, end_ip, None, None, email))
            cur.execute("INSERT INTO ip_addresses (ip_start, ip_end) VALUES (?, ?)", (start_ip, end_ip))
        elif '-' in ip_text:
            start, end = ip_text.split('-')
            asyncio.run(add_task(start.strip(), end.strip(), None, None, email))
            cur.execute("INSERT INTO ip_addresses (ip_start, ip_end) VALUES (?, ?)", (start.strip(), end.strip()))
        else:
            asyncio.run(add_task(ip_text, ip_text, None, None, email))
            cur.execute("INSERT INTO ip_addresses (ip_start, ip_end) VALUES (?, ?)", (ip_text, ip_text))
        conn.commit()

        ip_list.controls.append(ft.Text(ip_text))
        ip_input.value = ""
        page.update()

        # page.clean()
        # page.add(ft.Text("Data submitted successfully!"))
        # page.update()

    ip_input = ft.TextField(label="Enter IP Address (single, range, or CIDR)", width=400)
    add_button = ft.ElevatedButton("Запустить работу", on_click=start_work)
    ip_list = ft.Column()
    send_to_email = ft.Checkbox(label="Send to email", on_change=lambda e: page.update())
    email_input = ft.TextField(label="Enter email", width=400, visible=False)

    def send_to_email_changed(e):
        if send_to_email.value:
            email_input.visible = True
        else:
            email_input.visible = False
        page.update()

    send_to_email.on_change = send_to_email_changed

    input_section = ft.Column(
        [
            ft.Row(
                [ip_input],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [ip_list],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [send_to_email, email_input],
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