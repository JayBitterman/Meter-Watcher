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

    clients = []

    while True:
        # listen for clients
        # Client is a tuple of client (IP, Port)
        connection, new_client_address = server_socket.accept()
        # store IP address
        new_client_address = new_client_address[0]
        
        try:
            # Send message back to client in bytes
            user_msg = connection.recv(1024)
            print("Client Message: " + user_msg.decode())

            # park or tattle
            status = user_msg.decode().split(" ")[0]

            # Store new parked clients
            if status == "park" and new_client_address not in clients:
                clients.append(new_client_address)
            # Remove unparked clients
            elif status == "park" and new_client_address in clients:
                clients.remove(new_client_address)
            # Send tattle alert
            elif status == "tattle":
                for client in clients:
                    loc1 = geocoder.ipinfo(client[0]).latlng
                    loc2 = geocoder.ipinfo(new_client_address[0]).latlng
                    if geocoder.distance(loc1, loc2) < 1:
                        connection.send(bytes("Meter Maid in your area! Run!", encoding='UTF-8'))
                        
        except Exception as msg:
            print(msg)


if __name__ == "__main__":
    main()


