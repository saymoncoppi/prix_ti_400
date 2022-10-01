import socket
import datetime
import random
import time

HOST = "192.168.0.11"
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))


def sample_socket_answer():
    now = datetime.datetime.now()
    sample_platform_values = (
        "Plataforma",
        "checkwghr",
        "ABC",
        "12345",
        "BW321",
        "platform",
    )
    sample_platform = random.choice(sample_platform_values)
    sample_material = random.randrange(1, 999999999999)
    sample_weight = round(random.uniform(0.0, 6.999), 3)
    sample_weight_stable = "E"
    sample_date_time = now.strftime("%d/%m/%Y%H:%M:%S")
    sample_msg = (
        str(sample_platform).ljust(10, " ")
        + str(sample_weight).rjust(7, " ").replace(".", ",")
        + str(sample_weight_stable)
        + str("kg")
        + str(sample_date_time)
        + str(sample_material)
    )
    sample_msg = sample_msg.encode("utf-8")

    # sample_msg1 = "Plataforma  0,497Ekg26/09/202215:04:55       04321"
    return sample_msg


server.listen(5)
print(f"Simple Socket Server                    ({HOST}:{PORT})\n")

while True:
    communication_socket, address = server.accept()
    print(f"Conected to {address}")
    while 1:
        msg = sample_socket_answer()
        communication_socket.send(msg)
        print(f"Sent: {msg.decode()}")
        time.sleep(5)

    communication_socket.close()
