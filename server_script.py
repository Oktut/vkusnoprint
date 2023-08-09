import socket
import argparse
import subprocess
import os
import signal


def perform_operation(operator, num1, num2):
    # Выполняет арифметические операции (+, -, *, /) над двумя числами и возвращает результат.
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
    else:
        raise ValueError("Такого оператора у нас нет.")


def run_server():
    # Запускает сервер в новом процессе с помощью модуля subprocess.
    server_script = "server.py"
    server_process = subprocess.Popen(["python", server_script])
    return server_process


def main():
    parser = argparse.ArgumentParser(description="Клиент для удаленного калькулятора")
    parser.add_argument(
        "host",
        type=str,
        help="Адрес сервера"
    )
    parser.add_argument(
        "port",
        type=int,
        help="Порт сервера"
    )
    parser.add_argument(
        "operator",
        type=str,
        help="Оператор (+, -, '*', dell)"
    )
    parser.add_argument(
        "num1",
        type=float,
        help="Первое число"
    )
    parser.add_argument(
        "num2",
        type=float,
        help="Второе число"
    )
    args = parser.parse_args()

    # Преобразование оператора в '/' при использовании обозначения 'dell'
    if args.operator == "dell":
        args.operator = "/"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            data = f"{args.operator} {args.num1} {args.num2}".encode("utf-8")
            client_socket.sendto(data, (args.host, args.port))

            result, server_address = client_socket.recvfrom(1024)
            result = result.decode("utf-8")

            print(f"Результат: \033[34m{result}\033[0m\n")

        except socket.error as se:
            print(f"Ошибка: {se}")
            print("Нет связи с сервером. Запускаю сервер...")
            server_process = run_server()
            print("Сервер запущен. Попробуйте снова.")

            try:
                while True:
                    client_socket.sendto(data, (args.host, args.port))
                    result, server_address = client_socket.recvfrom(1024)
                    result = result.decode("utf-8")
                    print(f"Результат: \033[34m{result}\033[0m\n")
                    break
            except KeyboardInterrupt:
                print("Останавливаю сервер...")
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                print("Сервер остановлен.")
                exit(0)


if __name__ == "__main__":
    main()
