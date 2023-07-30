import socket as s
import geocoder
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/park')
def park():
    connect("park")
    return render_template('index.html')


@app.route('/tattle')
def tattle():
    connect("tattle")
    print('I tattled!')
    return render_template('index.html')


# Run code as script
def connect(request):
    # SOCK_STREAM = TCP
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # connect client to server IP and port
    address, port = "45.33.89.181", 6789
    client_socket.connect((address, port))

    try:
        # Receive data from server
        latlng = geocoder.ipinfo('me').latlng
        user_loc = str(latlng[0]) + " " + str(latlng[1]) + " " + str(request)
        client_socket.send(bytes(user_loc, encoding='UTF-8'))

    except Exception as msg:
        print(msg)

    finally:
        client_socket.close()


if __name__ == '__main__':
    app.run(debug=True)
