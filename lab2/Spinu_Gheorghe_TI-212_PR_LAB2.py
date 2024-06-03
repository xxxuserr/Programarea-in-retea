import socket
import threading

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

private_conversations = {}

def send_message_to_ip(message, ip, port):
    try:
        sock.sendto(message.encode(), (ip, port))
        print(f"Mesaj trimis '{message}' catre {ip}:{port}")
    except OSError as e:
        print("Error:", e)

def receive_messages():
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Mesaj primit de la {addr}: {data.decode()}")

def send_to_general_channel(message):
    send_message_to_ip(message, "224.0.0.1", UDP_PORT)
    print(f"Mesaj trimis '{message}' catre canalul general")

def receive_option():
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Mesaj primit de la {addr}: {data.decode()}")

# firurile de executie pentru primirea mesajelor 
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

receive_option_thread = threading.Thread(target=receive_option)
receive_option_thread.start()

while True:
    print("1. Mesaj catre un IP specific:")
    print("2. Mesaj catre canalul general:")
    choice = input("Introduceti ce fel de mesaj doriti: ")

    if choice == "1":
        dest_ip = input("Introduceti IP destinatar: ")
        message = input("Introduceti mesajul: ")
        send_message_to_ip(message, dest_ip, UDP_PORT)
    elif choice == "2":
        message = input("Introduceti mesajul: ")
        send_to_general_channel(message)
        pass
    else:
        print("Optiune incorecta!")
