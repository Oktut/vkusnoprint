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


def perform_operation(operator, num1, num2):    # Эта функция выполняет
    if operator == '+':                         # арифметические операции
        return num1 + num2                      # (+, -, *, /)
    elif operator == '-':                       # над двумя числами и
        return num1 - num2                      # возвращает результат.
    elif operator == '*':                       # Если операция деления (/)
        return num1 * num2                      # выполняется с нулевым
    elif operator == '/':                       # делителем, функция
        if num2 != 0:                           # вызывает исключение
            return num1 / num2                  # ValueError.
        else:
            raise ValueError("На ноль делить нельзя.")
    else:
        raise ValueError("Такого оператора у нас нет.")


def run_server():
    server_script = "server.py"
    server_process = subprocess.Popen(["python", server_script])
    return server_process


def main():
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

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            # отправляем данные на сервер
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
                # Если пользователь нажал Ctrl+C, останавливаем сервер и завершаем программу
                print("Останавливаю сервер...")
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                print("Сервер остановлен.")
                exit(0)


if __name__ == "__main__":
    main()
