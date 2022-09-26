import socket
import datetime
import random

HOST = '127.0.0.1'
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

def sample_socket_answer():
    now = datetime.datetime.now()
    sample_platform = 'Plataforma'
    sample_material = random.randrange(1, 999999999999)
    sample_weight = '  0,497'
    sample_weight_stable = 'E'
    sample_date_time = now.strftime('%d/%m/%Y%H:%M:%S') 
    sample_msg = str(sample_platform) + str(sample_weight) + str(sample_weight_stable) + str('kg') + str(sample_date_time) + str(sample_material)
    sample_msg = sample_msg.encode("utf-8")

    #sample_msg1 = "Plataforma  0,497Ekg26/09/202215:04:55       04321"
    return sample_msg


server.listen(5)
print(f"Simple Socket Server                    ({HOST}:{PORT})\n")

while True:
    communication_socket, address = server.accept()
    print(f"Conected to {address}")
    communication_socket.send(sample_socket_answer())
    print(f"Sent: {sample_socket_answer().decode()}")
    communication_socket.close()
