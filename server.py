import socket
import queue
import heapq

def perform_operation(operator, num1, num2):
    # Реализация perform_operation остается без изменений
    # ...

def main():
    host = "127.0.0.1"
    port = 5000

    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"Server started and listening on {host}:{port}")

        operation_queue = []  # Очередь с приоритетами на базе кучи (heap)

        while True:
            try:
                # Receive data from the client
                data, client_address = server_socket.recvfrom(1024)
                data = data.decode("utf-8")

                # Parse the data received from the client
                operator, num1, num2 = data.split()
                num1 = float(num1)
                num2 = float(num2)

                try:
                    # Perform the operation
                    result = perform_operation(operator, num1, num2)
                    response = str(result).encode("utf-8")
                except ValueError as ve:
                    # Handle errors
                    response = str(ve).encode("utf-8")

                # Add the operation to the priority queue
                # Priority is set to 0 for now, but can be adjusted based on requirements
                heapq.heappush(operation_queue, (0, response))

                # Process operations with highest priority first
                while operation_queue:
                    _, result_to_send = heapq.heappop(operation_queue)
                    server_socket.sendto(result_to_send, client_address)

            except KeyboardInterrupt:
                print("\nServer stopped.")
                break

if __name__ == "__main__":
    main()
