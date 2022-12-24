import threading
import socket
import time
from db import *

host = '127.0.0.1'
port = 9898
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

def broadcast(message):
    msg = 'ANN'+message
    for client in clients:
        client.send(msg.encode(FORMAT))

def recieve_choice(client, address, username):
    max_karata = 4 - get_tickets_by_user(username)
    client.send('ANNIzaberite neku od opcija\nLIST - broj preostalih karata\nRESERVE - rezervisati kartu\nRESERVE VIP - rezervisati kartu\nCANCEL TICKETS - otkazati kartu\nCANCEL VIP TICKETS - otkazati vip kartu\nIZLAZ - za izlaz iz aplikacije'.encode(FORMAT))

    try:
        while True:
            message = (client.recv(1024).decode(FORMAT)).upper()
            if message == 'LIST':
                client.send(f'ANNPreostalo je jos {get_all_tickets()} slobodnih obicnih karata kao i {get_all_vip_tickets()} vip karata.'.encode(FORMAT))
            elif message[:7] == 'RESERVE':
                unos = int(message[7:])
                if unos == 0:
                    client.send(f'ANNNiste rezervisali nijednu kartu!'.encode(FORMAT))
                elif ((max_karata != 0) and ((get_all_tickets())> 0) and (get_all_tickets()) - unos >= 0):
                    if ((max_karata-unos)<=0):
                        if(((get_all_tickets())-max_karata)<=0):
                            update_tickets_by_user(get_all_tickets(), username)
                        else:
                            update_tickets_by_user(max_karata, username)
                        time.sleep(0.2)
                        client.send(f'FANNRezervisan je maksimalan broj preostalih karata koje ste mogli da rezervisete ({max_karata})!'.encode(FORMAT))
                        print(f'{address} je rezervisao {max_karata} karte! Broj preostalih karata je {get_all_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_tickets()} karata!')
                        max_karata = 0
                    elif(get_all_tickets()==0):
                        client.send(f'ANNNema slobodnih karata!'.encode(FORMAT))                    
                    else:
                        update_tickets_by_user(unos, username)
                        max_karata -= unos
                        time.sleep(0.2)
                        client.send(f'FANNRezervisano je {unos} karata!'.encode(FORMAT))
                        print(f'{address} je rezervisao {unos} karte! Broj preostalih karata je {get_all_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_tickets()} karata!')
                else:
                    client.send(f'ANNRezervisan je maksimalan broj karata!'.encode(FORMAT))
            elif message[:11] == 'VIP_RESERVE':
                unos = int(message[11:])
                if ((max_karata != 0) and (((get_all_vip_tickets()) > 0) and ((get_all_vip_tickets()) - unos >= 0))):
                    if ((max_karata-unos)<=0):
                        if(((get_all_vip_tickets())-max_karata)<=0):
                            update_vip_tickets_by_user((get_all_vip_tickets()), username)
                        else:
                            update_vip_tickets_by_user(max_karata, username)
                        client.send(f'FANNRezervisan je maksimalan broj preostalih karata koje ste mogli da rezervisete ({max_karata})!'.encode(FORMAT))
                        print(f'{address} je rezervisao {max_karata} vip karte! Broj preostalih vip karata je {get_all_vip_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_vip_tickets()} vip karata!')
                        max_karata = 0 
                    elif(get_all_vip_tickets()==0):
                        client.send(f'ANNNema slobodnih vip karata!'.encode(FORMAT))                      
                    else:
                        update_vip_tickets_by_user(unos, username)
                        max_karata -= unos
                        client.send(f'FANNRezervisano je {unos} vip karata!'.encode(FORMAT))
                        print(f'{address} je rezervisao {unos} vip karte! Broj preostalih vip karata je {get_all_vip_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_vip_tickets()} vip karata!')
                else:
                    client.send(f'ANNRezervisan je maksimalan broj karata!'.encode(FORMAT))

            elif message[:8] == 'CANCEL_T':
                unos = int(message[8:])
                if unos == 0:
                    client.send(f'ANNNiste otkazali nijednu kartu!'.encode(FORMAT))
                elif ((max_karata >= 0 and max_karata < 4)):
                    if (((4-max_karata)-unos)<=0):
                        update_tickets_by_user(0, username)
                        client.send(f'FANNOtkazan je maksimalan broj karata ({4-max_karata})!'.encode(FORMAT))
                        time.sleep(0.2)
                        print(f'{address} je otkazao {4-max_karata} karte! Broj preostalih karata je {get_all_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_tickets()} karata!')
                        max_karata = 4                    
                    else:
                        max_karata += unos
                        update_tickets_by_user(4-max_karata, username)
                        time.sleep(0.2)
                        client.send(f'FANNOtkazano je {unos} karata!'.encode(FORMAT))
                        print(f'{address} je otkazao {unos} karte! Broj preostalih karata je {get_all_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_tickets()} karata!')
    
            elif message[:10] == 'CANCEL_V_T':
                unos = int(message[10:])
                if unos == 0:
                    client.send(f'ANNNiste otkazali nijednu kartu!'.encode(FORMAT))
                elif ((max_karata >= 0 and max_karata < 4)):
                    if (((4-max_karata)-unos)<=0):
                        update_vip_tickets_by_user(0, username)
                        client.send(f'FANNOtkazan je maksimalan broj karata ({4-max_karata})!'.encode(FORMAT))
                        time.sleep(0.2)
                        print(f'{address} je otkazao {4-max_karata} karte! Broj preostalih karata je {get_all_vip_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_vip_tickets()} vip karata!')
                        max_karata = 4                    
                    else:
                        max_karata += unos
                        update_vip_tickets_by_user(4-max_karata, username)
                        time.sleep(0.2)
                        client.send(f'FANNOtkazano je {unos} vip karata!'.encode(FORMAT))
                        print(f'{address} je otkazao {unos} karte! Broj preostalih karata je {get_all_vip_tickets()}.')
                        broadcast(f'Preostalo je jos {get_all_vip_tickets()} karata!')

                else:
                    client.send(f'ANNImate maksimalan broj karata!'.encode(FORMAT))


            elif message == 'IZLAZ':
                print(f'{str(address)} se diskonektovao!')
                client.close()
                break
            elif message == 'MAX_TICKETS':
                if max_karata != 0:
                    client.send((('MAX_TICKETS')+(str(max_karata))).encode(FORMAT))
                else:
                    time.sleep(0.2)
                    client.send((('MAX_TICKETS')+(str(0))).encode(FORMAT))

    except Exception as e:
        print(e)
        print(f'{str(address)} se diskonektovao!')
        client.close()

def check_message(client,message,br_slova):
    if len(message) <= br_slova:
        client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
        client.close()
        return True
    return False
    
def register_new_user(client, address):
    username_temp = str()
    password_temp = str()
    ime_temp = str()
    prezime_temp = str()
    jmbg_temp = int()
    email_temp = str()
    auth_complete = False
    print('SUCCESS REG')
    client.send('REG_U_NAMEUnesite Vase korisnicko ime:'.encode(FORMAT))
    while True:
        try:
            message_rcvd = client.recv(1024).decode(FORMAT)
            if message_rcvd[:6] == 'U_NAME':
                if check_message(client,message_rcvd,6):
                    return
                if not check_username(message_rcvd[6:]):
                    client.send('ANNIzabrali ste postojece korisnicko ime!'.encode(FORMAT))
                    client.send('REG_U_NAMEUnesite drugacije korisnicko ime:'.encode(FORMAT))
                else:
                    print('SUCCESS U_NAME')
                    username_temp = message_rcvd[6:]
                    client.send('REG_PASSWORDUnesite Vasu sifru:'.encode(FORMAT))

            if message_rcvd[:8] == 'PASSWORD':
                if check_message(client,message_rcvd,8):
                    return
                print('SUCCESS PASSWORD')
                password_temp = message_rcvd[8:]
                client.send('REG_NAMEUnesite Vase ime:'.encode(FORMAT))
            
            if message_rcvd[:4] == 'NAME':
                if check_message(client,message_rcvd,4):
                    return
                print('SUCCESS NAME')
                ime_temp = message_rcvd[4:]
                client.send('REG_L_NAMEUnesite Vase prezime:'.encode(FORMAT))

            if message_rcvd[:6] == 'L_NAME':
                if check_message(client,message_rcvd,6):
                    return
                print('SUCCESS L_NAME')
                prezime_temp = message_rcvd[6:]
                client.send('REG_JMBGUnesite Vas jmbg:'.encode(FORMAT))
            
            if message_rcvd[:4] == 'JMBG':
                if check_message(client,message_rcvd,4):
                    return
                print('SUCCESS JMBG')
                jmbg_temp = int(message_rcvd[4:])
                client.send('REG_EMAILUnesite Vasu e-mail adresu:'.encode(FORMAT))

            if message_rcvd[:5] == 'EMAIL':
                if check_message(client,message_rcvd,5):
                    return
                print('SUCCESS EMAIL')
                email_temp = message_rcvd[5:]
                client.send('ANNUspesno ste se registrovali na server!'.encode(FORMAT))
                client.send('AUTH_SUCCESS'.encode(FORMAT))
                auth_complete = True
                insert_new_user((username_temp, password_temp, ime_temp, prezime_temp, jmbg_temp, email_temp, 0, 0))
                break

        except Exception as e:
            print(e)
            print(f'{str(address)} se diskonektovao!')
            client.close()
            return

    if auth_complete:
        recieve_thread = threading.Thread(target=recieve_choice, args=(client, address, username_temp))
        recieve_thread.start()

def login_user(client, address):
    username_temp = str()
    complete = False
    print('SUCCESS LOGIN')
    client.send('LOGIN_U_NAMEUnesite Vase korisnicko ime:'.encode(FORMAT))
    while True:
        try:
            message_rcvd = client.recv(1024).decode(FORMAT)
            
            if message_rcvd[:6] == 'U_NAME':
                if check_message(client,message_rcvd,6):
                    return
                if not check_username(message_rcvd[6:]):
                    print('SUCCESS U_NAME')
                    username_temp = message_rcvd[6:]
                    client.send('LOGIN_PASSWORDUnesite Vasu sifru:'.encode(FORMAT))
                else:
                    client.send('ANNIzabrali ste nepostojece korisnicko ime!'.encode(FORMAT))
                    client.send('LOGIN_U_NAMEUnesite drugacije korisnicko ime:'.encode(FORMAT))

            if message_rcvd[:8] == 'PASSWORD':
                if check_message(client,message_rcvd,8):
                    return
                if check_password(username_temp, message_rcvd[8:]):
                    print('SUCCESS PASSWORD')
                    client.send('ANNUspesno ste se prijavili na server!'.encode(FORMAT))
                    client.send('AUTH_SUCCESS'.encode(FORMAT))
                    complete = True
                    break
                else:
                    client.send('ANNPogresna sifra!'.encode(FORMAT))
                    client.send('LOGIN_PASSWORDProbajte ponovo!'.encode(FORMAT))

        except Exception as e:
            print(e)
            print(f'{str(address)} se diskonektovao!')
            client.close()
            return
    if complete:
        recieve_thread = threading.Thread(target=recieve_choice, args=(client, address, username_temp))
        recieve_thread.start()

def connection():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f'Uspjesno povezan sa {str(address)}')
        init_thread = threading.Thread(target=init, args=(client, address))
        init_thread.start()


def init(client,address):
    try:
        client.send('Povezani ste sa serverom!\nIzaberite neku od opcija\nlogin - za postojeci nalog\nregister - za registraciju\nizlaz - za izlaz iz aplikacije'.encode(FORMAT))
        message_rcvd = client.recv(1024).decode(FORMAT)
        if message_rcvd == 'REG':
            register_thread = threading.Thread(target=register_new_user, args=(client, address))
            register_thread.start()
        elif message_rcvd == 'LOGIN':
            login_thread = threading.Thread(target=login_user, args=(client, address))
            login_thread.start()
    except:
        print(f'{str(address)} se diskonektovao!')
        clients.remove(client)
        client.close()
    


print("Server is listening...")
connection()





