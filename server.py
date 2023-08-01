import socket
import heapq


def perform_operation(operator, num1, num2):
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


def main():
    host = "127.0.0.1"
    port = 5000

    # Создаем UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"Сервер запущен и слушает на {host}:{port}")

        operation_queue = []  # Очередь с приоритетами (heap)

        while True:
            try:
                # Получение данных от клиента
                data, client_address = server_socket.recvfrom(1024)
                data = data.decode("utf-8")

                # Разбираем полученные данные от клиента
                operator, num1, num2 = data.split()
                num1 = float(num1)
                num2 = float(num2)

                try:
                    # Выполняем операцию
                    result = perform_operation(operator, num1, num2)
                    response = str(result).encode("utf-8")
                except ValueError as ve:
                    # Обрабатываем ошибки
                    response = str(ve).encode("utf-8")

                # Добавляем операцию в очередь с приоритетами
                # Приоритет пока установлен на 0, но может быть
                # изменен в зависимости от требований
                heapq.heappush(operation_queue, (0, response))

                # Обрабатываем операции с наивысшим приоритетом первыми
                while operation_queue:
                    _, result_to_send = heapq.heappop(operation_queue)
                    server_socket.sendto(result_to_send, client_address)

            except KeyboardInterrupt:
                print("\nСервер остановлен.")
                break


if __name__ == "__main__":
    main()
