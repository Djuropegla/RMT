import threading
import socket

FORMAT = 'utf-8'    
RESET = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9898))

# def broadcast():
#     print("IM ALIVE")
#     while True:
#         try:
#             message = client.recv(1024).decode(FORMAT)
#             if message == (message[:9]):
#                 print(message[9:])
#             else:
#                 continue
#         except:
#             print("Connection was terminated!")
#             client.close()
#             break

def rezervacija():
    global RESET
    while RESET:
        try:
            br_karata = int(input("Unesite broj karata koje zelite da rezervisete: "))
        except ValueError:
            print("Unos mora biti cijeli broj!")
        if br_karata > 0 and br_karata <= 4:
            return br_karata
            break
        if br_karata > 4:
            print("Maksimalan broj karata koje mozete da unesete je 4!")
            RESET = True
        if br_karata <= 0:
            print("Minimalan broj karata koje mozete da rezervisete je 1!")
            RESET = True
        else:
            print("GRESKA")
            client.close()
            break

def recieve():
    global RESET
    while RESET:
        try:
            msg = client.recv(1024).decode(FORMAT)

            if msg[:8] == 'GREETING':
                print(msg[8:])
            elif msg[:4] == 'LIST':
                print(msg[4:])
            elif msg[:7] == 'RESERVE':
                print(msg[7:])
            elif msg[:9] == 'BROADCAST':
                print(msg[9:])
        except:
            print("Veza sa serverom je prekinuta")
            client.close()
            input()
            break

# def list(izbor):
#     client.send(izbor.encode(FORMAT))

# def reserve(izbor):
#     client.send(izbor.encode(FORMAT))

def meni():
    global RESET
    while RESET:
        choice = f'{input()}'
        # choice = f'{input("Vas izbor: ")}'
        choice = choice.rstrip()
        if choice.upper() == 'LIST':
            # list(choice)
            client.send(choice.encode(FORMAT))
        elif choice.upper() == 'RESERVE':
            br = rezervacija()
            # reserve(choice+str(br))
            client.send((choice+str(br)).encode(FORMAT))
        elif choice.upper() == 'IZLAZ':
            RESET = False
            input()
            break

def auth_client():
    global RESET
    thread_dead = False
    print(client.recv(1024).decode(FORMAT))
    while RESET:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'Izaberite neku od opcija\nlogin - za postojeci nalog\nregister - za registraciju\nizlaz - za izlaz iz aplikacije':
                unos = input()
                client.send(unos.encode(FORMAT))
                
        except:
            print("Veza sa serverom je prekinuta")
            client.close()
            thread_dead = True
            input()
            break

    if thread_dead == False:
        recieve_thread = threading.Thread(target=recieve)
        meni_thread = threading.Thread(target=meni)

        recieve_thread.start()
        meni_thread.start()
            



print("im client")
auth_client()



