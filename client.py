import threading
import socket

FORMAT = 'utf-8'    
RESET = True
MAX_TICKETS = int()

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
    global MAX_TICKETS
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
            elif msg[:3] == 'ANN':
                print(msg[3:])
            elif msg[:11] == 'MAX_TICKETS':
                MAX_TICKETS = int(msg[11:])
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
        client.send('MAX_TICKETS'.encode(FORMAT))
        choice = f'{input()}'
        # choice = f'{input("Vas izbor: ")}'
        choice = choice.rstrip()
        if choice.upper() == 'LIST':
            # list(choice)  
            client.send(choice.encode(FORMAT))
        elif choice.upper() == 'RESERVE':
            # br = rezervacija()
            # reserve(choice+str(br))
            print(f'Unesite broj karata koje zelite da rezervisete (mozete rezervisati {MAX_TICKETS}):')
            while True:
                try:
                    br = int(input())
                    break
                except:
                    print('Mozete unositi samo brojeve!')
            client.send((choice+str(br)).encode(FORMAT))
            # client.send('MAX_TICKETS'.encode(FORMAT))
        elif choice.upper() == 'IZLAZ':
            RESET = False
            input()
            break
        else:
            print("Pogresan unos!")

def auth_client():
    global RESET
    auth_complete = False
    # alive = True
    # print(client.recv(1024).decode(FORMAT))
    # alive = True
    while True:
        try:
            message_rcvd = client.recv(1024).decode(FORMAT)
            if message_rcvd[:3] == 'ANN':
                print(message_rcvd[3:])
            if message_rcvd[:8] == 'GREETING':
                print(message_rcvd[8:])
                while True:
                    try:
                        message = input().upper()
                        if message == 'REGISTER':
                            client.send('REG'.encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo:')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()

            # if message_rcvd[:10] == 'REG_U_NAME':
            #     print(message_rcvd[10:])
            #     message = input()
            #     if ((len(message) > 0) and (len(message) < 20)):
            #         client.send(('U_NAME'+message).encode(FORMAT))
            
            if message_rcvd[:10] == 'REG_U_NAME':
                print(message_rcvd[10:])
                while True:
                    try:
                        message = input()
                        if ((len(message) > 0) and (len(message) < 20)):
                            client.send(('U_NAME'+message).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo:')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()
            
            if message_rcvd[:12] == 'REG_PASSWORD':
                print(message_rcvd[12:])
                while True:
                    try:
                        message = input()
                        if ((len(message) > 0) and (len(message) < 20)):
                            client.send(('PASSWORD'+message).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo:')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()
            
            if message_rcvd[:8] == 'REG_NAME':
                print(message_rcvd[8:])
                while True:
                    try:
                        message = input()
                        if ((len(message) > 0) and (len(message) < 20)):
                            client.send(('NAME'+message).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo:')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()

            if message_rcvd[:10] == 'REG_L_NAME':
                print(message_rcvd[10:])
                while True:
                    try:
                        message = input()
                        if ((len(message) > 0) and (len(message) < 20)):
                            client.send(('L_NAME'+message).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo: ')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()

            if message_rcvd[:8] == 'REG_JMBG':
                print(message_rcvd[8:])
                while True:
                    try:
                        while True:
                            try:
                                message = int(input())
                                break
                            except:
                                print('Mozete unositi samo brojeve!')
                        
                        if (len(str(message)) == 13):
                            client.send(('JMBG'+(str(message))).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo: ')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()

            if message_rcvd[:9] == 'REG_EMAIL':
                print(message_rcvd[9:])
                while True:
                    try:
                        message = input()
                        if ((len(message) > 0) and (len(message) < 20)):
                            client.send(('EMAIL'+message).encode(FORMAT))
                            break
                        else:
                            print('Greska! Pokusajte ponovo: ')
                    except:
                        print('KONEKCIJA PREKIINUTA')
                        client.close()

            if message_rcvd[:12] == 'AUTH_SUCCESS':
                # print(message_rcvd[12:])
                print("EVE GA NA KRAJU")
                auth_complete = True
                break

                # while alive:
                #     message = input()
                #     if ((len(message) > 0) and (len(message) < 20)):
                #         client.send(('NAME'+message).encode(FORMAT))
                #         alive = False
                #     else:
                #         print('Greska! Pokusajte ponovo: ')
                #     alive = True
            # if message == 'Izaberite neku od opcija\nlogin - za postojeci nalog\nregister - za registraciju\nizlaz - za izlaz iz aplikacije':
            #     unos = input()
            #     client.send(unos.encode(FORMAT)) 
        except:
            print("Veza sa serverom je prekinuta")
            client.close()
            thread_dead = True
            input()
            break
    if auth_complete:
        recieve_thread = threading.Thread(target=recieve)
        meni_thread = threading.Thread(target=meni)

        recieve_thread.start()
        meni_thread.start()
            



print("im client")
auth_client()



