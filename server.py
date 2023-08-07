import threading
import socket as s
import geocoder


def handle_client(connection, address, clients):
    try:
        # Send message back to client in bytes
        user_msg = connection.recv(1024)
        print("Client Message: " + user_msg.decode())

        # park or tattle
        status = user_msg.decode()

        # Store new parked clients
        if status == "park" and address not in clients:
            clients.append(address)
        # Remove unparked clients
        elif status == "park" and address in clients:
            clients.remove(address)
        # Send tattle alert
        elif status == "tattle":
            print(clients)
            for client in clients:
                loc1 = geocoder.ipinfo(client).latlng
                loc2 = geocoder.ipinfo(address).latlng
                if geocoder.distance(loc1, loc2) < 1:
                    connection.send(bytes("Meter Maid in your area! Run!", encoding='UTF-8'))
    except Exception as msg:
        print(msg)
    finally:
        connection.close()


def main():
    # SOCK_STREAM = TCP
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    address, port = "", 6789
    server_socket.bind((address, port))

    # maximum of 5 connections
    server_socket.listen(5)
    print("Server is open.")

    clients = []

    while True:
        # listen for clients
        # Client is a tuple of client (IP, Port)
        connection, new_client_address = server_socket.accept()
        # store IP address
        new_client_address = new_client_address[0]
        print(new_client_address)

        # Handle each client in a new thread
        threading.Thread(target=handle_client, args=(connection, new_client_address, clients)).start()


if __name__ == "__main__":
    main()
