import socket


def main():
    host = "127.0.0.1"  # Адрес сервера (локальный хост)
    port = 5000  # Порт сервера

    # Создаем UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            # Получаем ввод от пользователя
            operator = input(
                            "Введите оператор (+, -, *, /) or 'q' to quit: "
                            )
            if operator == 'q':
                break

            while True:
                try:
                    num1 = float(input("Введите первое число: "))
                    break  # Если успешно преобразовали, выходим из цикла
                except ValueError:
                    print("Ошибка! Введите корректное число.")

            while True:
                try:
                    num2 = float(input("Введите второе число: "))
                    break  # Если успешно преобразовали, выходим из цикла
                except ValueError:
                    print("Ошибка! Введите корректное число.")

            # Подготавливаем данные для отправки на сервер
            data = f"{operator} {num1} {num2}".encode("utf-8")

            try:
                # Отправляем данные на сервер
                client_socket.sendto(data, (host, port))

                # Получаем результат от сервера
                result, server_address = client_socket.recvfrom(1024)
                result = result.decode("utf-8")

                # Выводим результат на экран
                print(f"Результат: {result}")
            except KeyboardInterrupt:
                print("\nCКлиент остановлен.")
                break


if __name__ == "__main__":
    main()
