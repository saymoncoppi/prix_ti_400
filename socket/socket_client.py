"""
"""
import socket
import argparse
from datetime import datetime
import time
from pathlib import Path
import os

parser = argparse.ArgumentParser(description="Connect to PRIX TI400 Socket Server")
parser.add_argument("-ip", "--ip_address", required=True)
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-l", "--log", choices=["yes", "no"], default="yes", required=True)
options = parser.parse_args()

tcp_ip = str(options.ip_address)
tcp_port = int(options.port)
log = str(options.log)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = (tcp_ip, tcp_port)

BUFFER_SIZE = 1024

current_data = ""
ext_platform = ""
ext_material = ""
ext_weight = ""
ext_weight_stable = ""
ext_date_time = ""
received_changes = ""
check_changes = ""
is_connected = False


def logger(received_data):
    """Function to write log files"""
    target_folder = Path("log")
    now = datetime.now()

    if not os.path.exists(target_folder):
        Path("log").mkdir(parents=True, exist_ok=True)

    txt_filename = "LOG_" + now.strftime("%Y%m%d%H%M%S") + ".txt"
    new_txt = Path(target_folder, str(txt_filename))
    txt_lines = []
    txt_lines.append(f"{received_data}\n")

    f = open(new_txt, "w")
    f.writelines(txt_lines)
    f.close()

    print(f"Writing log file: {new_txt}\n")
    return


try:
    tcp.connect(connection)
    print()
    print(f"Conencted on {tcp_ip}:{tcp_port}")
    print("======================================================================")
    print()
    is_connected = True
except:
    print()
    print(f"Cannot conenct to {tcp_ip}:{tcp_port}")
    print()

if is_connected:
    while 1:
        received_data = tcp.recv(BUFFER_SIZE).decode()

        if received_data:
            # Sample data: Plataforma  0,497Ekg26/09/202215:04:55       04321
            if len(received_data) == 50:
                ext_platform = received_data[:10].rstrip()
                ext_material = received_data[-12:].lstrip()
                ext_weight = received_data[10:17].lstrip().replace(",", ".")
                ext_weight_stable = received_data[17:18].lstrip()
                ext_date_time_pre = received_data[20:38].lstrip()
                ext_date_time = datetime.strptime(ext_date_time_pre, "%d/%m/%Y%H:%M:%S")
                if ext_material:
                    received_changes = f"{ext_material}|{ext_weight}"
                else:
                    print(
                        f"Invalid Material! {ext_material} \nWaiting 5 seconds to try again...\n"
                    )
                    time.sleep(5)

                # if not check_changes == received_changes:
                if (
                    (ext_weight_stable == "E")
                    and (not ext_weight == "0.000")
                    and (not check_changes == received_changes)
                ):
                    check_changes = f"{ext_material}|{ext_weight}"
                    cur_platform = ext_platform
                    cur_material = ext_material
                    cur_weight_stable = ext_weight_stable
                    cur_weight = ext_weight
                    cur_date_time = ext_date_time

                    print(f"Platform:   {cur_platform}")
                    print(f"Material:   {cur_material}")
                    print(f"Weight:     {cur_weight}")
                    print(f"Date/Time:  {cur_date_time}")
                    print(
                        "----------------------------------------------------------------------"
                    )

                    if log == "yes":
                        logger(received_data)

    tcp.close()
