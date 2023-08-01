import socket


def main():
    host = "127.0.0.1"
    port = 5000

    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            # Get input from the user
            operator = input(
                            "Enter the operator (+, -, *, /) or 'q' to quit: "
                            )
            if operator == 'q':
                break

            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            # Prepare the data to be sent to the server
            data = f"{operator} {num1} {num2}".encode("utf-8")

            try:
                # Send the data to the server
                client_socket.sendto(data, (host, port))

                # Receive the result from the server
                result, server_address = client_socket.recvfrom(1024)
                result = result.decode("utf-8")

                # Display the result
                print(f"Result: {result}")
            except KeyboardInterrupt:
                print("\nClient stopped.")
                break


if __name__ == "__main__":
    main()
