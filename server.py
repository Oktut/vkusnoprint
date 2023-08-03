# Код представляет собой реализацию "удаленного калькулятора" на базе
# UDP-сокетов. Он позволяет клиенту отправлять операции и числа на сервер,
# сервер выполняет эти операции и возвращает результат обратно клиенту. Весь
# обмен данными между клиентом и сервером происходит через
# сетевой протокол UDP.
import socket
# Модуль socket предоставляет функциональность для работы с сетевыми сокетами,
# позволяя программам обмениваться данными через сеть. В данном коде
# используется для создания UDP-сокета (socket.AF_INET - семейство адресов для
# сети IPv4, socket.SOCK_DGRAM - тип сокета для протокола UDP), привязки сокета
# к указанному адресу и порту, а также для отправки и получения данных от
# клиентов на сервере.
import heapq
# Модуль heapq предоставляет функции для работы с кучей (heap) - это
# специальная структура данных, которая обеспечивает быстрый доступ к
# наименьшему или наибольшему элементу в коллекции. В данном коде используется
# для реализации очереди с приоритетами на базе кучи. Операции отправленные от
# клиентов помещаются в эту очередь с приоритетом 0, и сервер обрабатывает
# операции с наивысшим приоритетом первыми. Таким образом, куча помогает
# гарантировать, что операции будут обрабатываться в правильном порядке,
# согласно приоритету.


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
    else:
        raise ValueError("Такого оператора у нас нет.")


def main():
    # Функция main() определяет адрес и порт, на которых будет работать сервер
    host = "127.0.0.1"
    port = 5000

    # Создаем UDP-сокет (server_socket) и привязывает его к указанному адресу
    # и порту для прослушивания входящих пакетов от клиентов.
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
