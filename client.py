import socket


def main():
    host = "127.0.0.1"  # Адрес сервера (локальный хост)
    port = 5000  # Порт сервера

    # Создаем UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            # Получаем ввод от пользователя для оператора
            while True:
                operator = input(
                    "Введите оператор \033[31m(+, -, *, /)\033[0m or \033[31m'q'\033[0m to quit: \n"
                )
                if operator in ['+', '-', '*', '/', 'q']:
                    break
                else:
                    print("\033[33mОшибка!\033[0m Введите корректный оператор \033[31m(+, -, *, /)\033[0m or \033[31m'q'\033[0m to quit: \n")

            if operator == 'q':
                break

            while True:
                try:
                    num1 = float(input("Введите первое число: \n"))
                    break  # Если успешно преобразовали, выходим из цикла
                except ValueError:
                    print("Ошибка! Введите корректное число.\n")

            while True:
                try:
                    num2 = float(input("Введите второе число: \n"))
                    break  # Если успешно преобразовали, выходим из цикла
                except ValueError:
                    print("Ошибка! Введите корректное число.\n")

            # Подготавливаем данные для отправки на сервер
            data = f"{operator} {num1} {num2}".encode("utf-8")

            try:
                # Отправляем данные на сервер
                client_socket.sendto(data, (host, port))

                # Получаем результат от сервера
                result, server_address = client_socket.recvfrom(1024)
                result = result.decode("utf-8")

                # Форматируем вывод результата в зависимости от типа числа
                if num1.is_integer() and num2.is_integer():
                    formatted_result = str(int(float(result)))
                else:
                    formatted_result = result

                # Выводим результат на экран
                print(f"Результат: \033[34m{formatted_result}\033[0m\n")

            except KeyboardInterrupt:
                print("\nCКлиент остановлен.")
                break


if __name__ == "__main__":
    main()
