import threading
import socket
import time

host = '127.0.0.1'
port = 9898
FORMAT = 'utf-8'

BROJ_KARATA = 20
BROJ_VIP_KARATA = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()



clients = []

username_list = []
password_list = []
ime_list = []
prezime_list = []
jmbg_list = []
email_list = []
username_list.append('nikola123')
password_list.append('passnidzo')
ime_list.append('Nikola')
prezime_list.append('Nikolic')
jmbg_list.append(1234)
email_list.append('nikolanikolic@gmail.com')
username_list.append('pavleggez')
password_list.append('passpavle')
ime_list.append('Pavle')
prezime_list.append('Pavlovic')
jmbg_list.append(4567)
email_list.append('pavle.pavlovic8@gmail.com')
username_list.append('alomilos')
password_list.append('passmilos')
ime_list.append('Milos')
prezime_list.append('Milosevic')
jmbg_list.append(3956)
email_list.append('milos486@gmail.com')

def rezervisi(br_karata):
    br_karata = int(br_karata)
    global BROJ_KARATA
    BROJ_KARATA = BROJ_KARATA - br_karata

def rezervisi_vip(br_karata):
    br_karata = int(br_karata)
    global BROJ_VIP_KARATA
    BROJ_VIP_KARATA = BROJ_VIP_KARATA - br_karata

def broadcast(message):
    msg = 'BROADCAST'+message
    for client in clients:
        client.send(msg.encode(FORMAT))

def recieve_choice(client, address):
    max_karata = 4
    client.send('GREETINGIzaberite neku od opcija\nLIST - broj preostalih karata\nRESERVE - rezervisati kartu\nRESERVE VIP - rezervisati kartu\nIZLAZ - za izlaz iz aplikacije'.encode(FORMAT))

    try:
        while True:
            message = (client.recv(1024).decode(FORMAT)).upper()
            if message == 'LIST':
                client.send(f'LISTPreostalo je jos {BROJ_KARATA} slobodnih karata.'.encode(FORMAT))
            elif message[:7] == 'RESERVE':
                unos = int(message[7:])
                if ((max_karata != 0) and ((BROJ_KARATA > 0) and (BROJ_KARATA - unos >= 0))):
                    if ((max_karata-unos)<=0):
                        rezervisi(max_karata)
                        client.send(f'ANNRezervisan je maksimalan broj preostalih karata koje ste mogli da rezervisete ({max_karata})!'.encode(FORMAT))
                        print(f'{address} je rezervisao {max_karata} karte! Broj preostalih karata je {BROJ_KARATA}.')
                        broadcast(f'Preostalo je jos {BROJ_KARATA} karata!')
                        max_karata = 0                    
                    else:
                        rezervisi(unos)
                        max_karata -= int(unos)
                        print(f'{address} je rezervisao {unos} karte! Broj preostalih karata je {BROJ_KARATA}.')
                        broadcast(f'Preostalo je jos {BROJ_KARATA} karata!')
                else:
                    client.send(f'ANNRezervisan je maksimalan broj karata!'.encode(FORMAT))
            elif message[:11] == 'VIP_RESERVE':
                print("primljeno")
                print(message)
                unos = int(message[11:])
                if ((max_karata != 0) and ((BROJ_VIP_KARATA > 0) and (BROJ_VIP_KARATA - unos >= 0))):
                    if ((max_karata-unos)<=0):
                        rezervisi_vip(max_karata)
                        client.send(f'ANNRezervisan je maksimalan broj preostalih karata koje ste mogli da rezervisete ({max_karata})!'.encode(FORMAT))
                        print(f'{address} je rezervisao {max_karata} vip karte! Broj preostalih vip karata je {BROJ_VIP_KARATA}.')
                        broadcast(f'Preostalo je jos {BROJ_VIP_KARATA} vip karata!')
                        max_karata = 0                    
                    else:
                        rezervisi_vip(unos)
                        max_karata -= int(unos)
                        print(f'{address} je rezervisao {unos} vip karte! Broj preostalih vip karata je {BROJ_VIP_KARATA}.')
                        broadcast(f'Preostalo je jos {BROJ_VIP_KARATA} vip karata!')
                else:
                    client.send(f'ANNRezervisan je maksimalan broj karata!'.encode(FORMAT))
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

def login_provjera(username, password):
    result = False
    for user in username_list:
        if user == username:
            result = True
            break
    if result == False:
        return result
    for passw in password_list:
        if passw == password:
            break
        result = False
    return result

def check_message(client,message,br_slova):
    if len(message) <= br_slova:
        client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
        client.close()
        return True
    return False

def check_username(username_temp):
    for username in username_list:
        if username == username_temp:
            return True
    return False
        
def auth(client, address):
    username_temp = str()
    password_temp = str()
    ime_temp = str()
    prezime_temp = str()
    jmbg_temp = int()
    email_temp = str()
    auth_complete = False
    client.send('GREETINGPovezani ste sa serverom!\nIzaberite neku od opcija\nlogin - za postojeci nalog\nregister - za registraciju\nizlaz - za izlaz iz aplikacije'.encode(FORMAT))
    while True:
        try:
            message_rcvd = client.recv(1024).decode(FORMAT)

            if message_rcvd[:3] == 'REG':
                print('SUCCESS REG')
                client.send('REG_U_NAMEUnesite Vase korisnicko ime:'.encode(FORMAT))
            
            if message_rcvd[:6] == 'U_NAME':
                if check_message(client,message_rcvd,6):
                    return
                # if len(message_rcvd) == 6:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                if check_username(message_rcvd[6:]):
                    client.send('ANNIzabrali ste postojece korisnicko ime!'.encode(FORMAT))
                    client.send('REG_U_NAMEUnesite drugacije korisnicko ime:'.encode(FORMAT))
                else:
                    print('SUCCESS U_NAME')
                    username_temp = message_rcvd[6:]
                    client.send('REG_PASSWORDUnesite Vasu sifru:'.encode(FORMAT))

            if message_rcvd[:8] == 'PASSWORD':
                if check_message(client,message_rcvd,8):
                    return
                # if len(message_rcvd) == 8:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                print('SUCCESS PASSWORD')
                password_temp = message_rcvd[8:]
                client.send('REG_NAMEUnesite Vase ime:'.encode(FORMAT))
            
            if message_rcvd[:4] == 'NAME':
                if check_message(client,message_rcvd,4):
                    return
                # if len(message_rcvd) == 4:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                print('SUCCESS NAME')
                ime_temp = message_rcvd[4:]
                client.send('REG_L_NAMEUnesite Vase prezime:'.encode(FORMAT))

            if message_rcvd[:6] == 'L_NAME':
                if check_message(client,message_rcvd,6):
                    return
                # if len(message_rcvd) == 6:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                print('SUCCESS L_NAME')
                prezime_temp = message_rcvd[6:]
                client.send('REG_JMBGUnesite Vas jmbg:'.encode(FORMAT))
            
            if message_rcvd[:4] == 'JMBG':
                if check_message(client,message_rcvd,4):
                    return
                # if len(message_rcvd) == 4:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                print('SUCCESS JMBG')
                jmbg_temp = int(message_rcvd[4:])
                # print(jmbg_temp)
                # print(type(jmbg_temp))
                client.send('REG_EMAILUnesite Vasu e-mail adresu:'.encode(FORMAT))

            if message_rcvd[:5] == 'EMAIL':
                if check_message(client,message_rcvd,5):
                    return
                # if len(message_rcvd) == 5:
                #     client.send('NEAUTORIZOVAN PRISTUP!'.encode(FORMAT))
                #     client.close()
                #     return
                print('SUCCESS EMAIL')
                email_temp = message_rcvd[5:]
                client.send('ANNUspesno ste se registrovali na server!'.encode(FORMAT))
                client.send('AUTH_SUCCESS'.encode(FORMAT))
                auth_complete = True
                break

        except:
            print(f'{str(address)} se diskonektovao!')
            client.close()
            return

    if auth_complete:
        recieve_thread = threading.Thread(target=recieve_choice, args=(client, address))
        recieve_thread.start()

def connection():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f'Uspjesno povezan sa {str(address)}')
        auth_thread = threading.Thread(target=auth, args=(client, address))
        auth_thread.start()







print("Server is litening...")
# registracija_thread = threading.Thread(target=registracija)
# registracija_thread.start()
connection()





