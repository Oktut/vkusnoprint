import socket
# Модуль socket для работы с сокетами и
# обмена данными между клиентом и сервером.
import argparse
# Модуль argparse используется для обработки аргументов
# командной строки, переданных при запуске клиента.
import subprocess
# Модуль subprocess позволяет запускать сервер из
# командной строки и управлять им (в данном случае, остановка сервера).
import os
# Модуль os предоставляет функции для работы с операционной системой.
# Используется функцию os.killpg, которая позволяет отправить сигнал
# остановки (SIGTERM) всей группе процессов, которую представляет сервер.
import signal
# Модуль signal предоставляет функции для работы с сигналами.
# В данном случае, мы используем сигнал SIGTERM, который является сигналом
# остановки (termination). Этот сигнал используется для контролируемого
# завершения процессов, чтобы они могли корректно завершить свою работу
# перед остановкой.


def perform_operation(operator, num1, num2):
    # Эта функция выполняет арифметические операции (+, -, *, /)
    # над двумя числами и возвращает результат.
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 != 0:
            return num1 / num2
        else:
            raise ValueError("На ноль делить нельзя.")
        # Если операция деления (/) выполняется с нулевым делителем,
        # функция вызывает исключение ValueError.
    else:
        raise ValueError("Такого оператора у нас нет.")


def run_server():
    # Данная функция запускает сервер в новом процессе с помощью модуля
    # subprocess.
    server_script = "server.py"
    server_process = subprocess.Popen(["python", server_script])
    # Она возвращает объект subprocess.Popen, который представляет запущенный
    # процесс сервера. Этот объект позволяет нам управлять сервером и, при
    # необходимости, останавливать его.
    return server_process


def main():
    # Данная функция парсит аргументы командной строки, которые переданы при
    # запуске клиента. Аргументы включают адрес сервера, порт, оператор и
    # числа для выполнения операции.
    parser = argparse.ArgumentParser(description="Remote Calculator Client")
    parser.add_argument(
        "host",
        type=str,
        help="Server address"
    )
    parser.add_argument(
        "port",
        type=int,
        help="Server port"
    )
    parser.add_argument(
        "operator",
        type=str,
        choices=["+", "-", "*", "/"],
        help="Operator (+, -, *, /)"
    )
    parser.add_argument(
        "num1",
        type=float,
        help="First number"
    )
    parser.add_argument(
        "num2",
        type=float,
        help="Second number"
    )
    args = parser.parse_args()

    # Создает UDP-сокет для обмена данными с сервером.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            # Попытка отправить запрос на сервер с переданными
            # оператором и числами.
            data = f"{args.operator} {args.num1} {args.num2}".encode("utf-8")
            client_socket.sendto(data, (args.host, args.port))

            # получаем результаты с сервера
            result, server_address = client_socket.recvfrom(1024)
            result = result.decode("utf-8")

            # выводим результат
            print(f"Result: {result}")

        except socket.error as se:
            print(f"Ошибка: {se}")
            print("Нет связи с сервером. Запускаю сервер...")
            server_process = run_server()
            print("Сервер запущен. Попробуйте снова.")

            try:
                while True:
                    # Пробуем еще раз отправить запрос на сервер
                    client_socket.sendto(data, (args.host, args.port))
                    result, server_address = client_socket.recvfrom(1024)
                    result = result.decode("utf-8")
                    print(f"Result: {result}")
                    break
            except KeyboardInterrupt:
                # Если пользователь нажал Ctrl+C, останавливаем
                # сервер и завершаем программу
                print("Останавливаю сервер...")
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                print("Сервер остановлен.")
                exit(0)
                # При нажатии Ctrl+C, клиент останавливает сервер и успешно
                # завершает свою работу без ошибок


if __name__ == "__main__":
    main()
