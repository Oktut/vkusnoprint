import socket
import argparse
import subprocess


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


def run_server():
    server_script = "server.py"
    subprocess.Popen(["python", server_script])


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
            # Send the data to the server
            data = f"{args.operator} {args.num1} {args.num2}".encode("utf-8")
            client_socket.sendto(data, (args.host, args.port))

            # Receive the result from the server
            result, server_address = client_socket.recvfrom(1024)
            result = result.decode("utf-8")

            # Display the result
            print(f"Result: {result}")

        except socket.error as se:
            print(f"Error: {se}")
            print("Could not connect to the server. Starting the server...")
            run_server()
            print("Server started. Please try again.")


if __name__ == "__main__":
    main()
