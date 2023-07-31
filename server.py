import socket as s
import geocoder


# Run as a script rather than a module
def main():
    # SOCK_STREAM = TCP
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    address, port = "", 6789
    server_socket.bind((address, port))

    # maximum of 5 connections
    server_socket.listen(5)
    print("Server is open.")

    while True:
        # listen for clients
        connection, client_address = server_socket.accept()
        try:
            # send message to client in bytes
            user_msg = connection.recv(1024)
            print("Client Message: " + user_msg.decode())
        except Exception as msg:
            print(msg)
        finally:
            connection.close()


if __name__ == "__main__":
    main()


