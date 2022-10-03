#! /usr/bin/env python
"""
Program to extract data from PRIX TI400 Socket Server

Run:
socket_client.py -ip 192.168.0.x -p 9000

Sample answer from TI400:
Plataforma  0,497Ekg26/09/202215:04:55       04321

... Check the manual to see all possible parameters
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
parser.add_argument("-l", "--log", choices=["yes", "no"], default="yes")
parser.add_argument("-d", "--display", choices=["yes", "no"], default="no")
options = parser.parse_args()

tcp_ip = str(options.ip_address)
tcp_port = int(options.port)
log = str(options.log)
display = str(options.display)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = (tcp_ip, tcp_port)

BUFFER_SIZE = 1024

current_data = None
ext_platform = ""
ext_material = ""
ext_weight = ""
ext_weight_stable = ""
ext_date_time = ""
received_changes = ""
check_changes = ""
is_connected = False
cleanned_content = {}


def cleanned_data(received_data):
    cleanned_content["get_platform"] = received_data[:10].rstrip()
    cleanned_content["get_material"] = received_data[-12:].lstrip().replace(" ", "")
    cleanned_content["get_weight"] = received_data[10:17].lstrip().replace(",", ".")
    cleanned_content["get_weight_stable"] = received_data[17:18].lstrip()
    cleanned_content["get_date_time_pre"] = received_data[20:38].lstrip()
    cleanned_content["get_date_time"] = datetime.strptime(
        cleanned_content["get_date_time_pre"], "%d/%m/%Y%H:%M:%S"
    )

    return cleanned_content


def logger(logger_data):
    """Function to write log files"""
    target_folder = Path("log")
    now = datetime.now()

    if not os.path.exists(target_folder):
        Path("log").mkdir(parents=True, exist_ok=True)

    txt_filename = "LOG_" + now.strftime("%Y%m%d") + ".txt"
    new_txt = Path(target_folder, str(txt_filename))
    txt_lines = []
    txt_lines.append(f"{logger_data}\n")

    f = open(new_txt, "a")
    f.writelines(txt_lines)
    f.close()

    print(f"Writing log file: {new_txt}\n")
    return


def display_data(display_data_content):
    """Function to display data content during console execution"""
    for key in display_data_content:
        display_key = str(key).ljust(10, " ")
        print(display_key, "  :  ", display_data_content[key])
    print("----------------------------------------------------------------------")
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

        if len(received_data) == 50:

            cleanned_data(received_data)
            ext_platform = cleanned_content["get_platform"]
            ext_material = cleanned_content["get_material"]
            ext_weight = cleanned_content["get_weight"]
            ext_weight_stable = cleanned_content["get_weight_stable"]
            ext_date_time = cleanned_content["get_date_time"]

            if not ext_material == "":
                received_changes = f"{ext_material}|{ext_weight}"
                logger_data = (
                    f"{ext_platform};{ext_material};{ext_weight};{ext_date_time}"
                )
                display_data_content = {
                    "Platform": ext_platform,
                    "Material": ext_material,
                    "Weight": ext_weight,
                    "Date/Time": ext_date_time,
                }

            if (
                (ext_weight_stable == "E")
                and (not ext_weight == "0.000")
                and (not ext_material == "")
                and (not check_changes == received_changes)
            ):
                check_changes = f"{ext_material}|{ext_weight}"

                if display == "yes":
                    display_data(display_data_content)

                if log == "yes":
                    logger(logger_data)

    tcp.close()
