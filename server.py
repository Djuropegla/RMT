import threading
import socket

host = '127.0.0.1'
port = 9898
FORMAT = 'utf-8'

BROJ_KARATA = 20

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

username_list = []
password_list = []
ime_list = []
prezime_list = []
jmbg = []
email = []
username_list.append('nikola123')
password_list.append('passnidzo')
ime_list.append('Nikola')
prezime_list.append('Nikolic')
jmbg.append(1234)
email.append('nikolanikolic@gmail.com')
username_list.append('pavleggez')
password_list.append('passpavle')
ime_list.append('Pavle')
prezime_list.append('Pavlovic')
jmbg.append(4567)
email.append('pavle.pavlovic8@gmail.com')
username_list.append('alomilos')
password_list.append('passmilos')
ime_list.append('Milos')
prezime_list.append('Milosevic')
jmbg.append(3956)
email.append('milos486@gmail.com')

def rezervisi(br_karata):
    br_karata = int(br_karata)
    global BROJ_KARATA
    BROJ_KARATA = BROJ_KARATA - br_karata

def broadcast(message):
    msg = 'BROADCAST'+message
    for client in clients:
        client.send(msg.encode(FORMAT))

def recieve_choice(client, address):
    try:
        while True:
            message = client.recv(1024).decode(FORMAT)
            if message.upper() == 'LIST':
                client.send(f'LISTPreostalo je jos {BROJ_KARATA} slobodnih karata.'.encode(FORMAT))
            elif message.upper()[:7] == 'RESERVE':
                unos = message[7:]
                rezervisi(unos)
                print(f'{address} je rezervisao {unos} karte! Broj preostalih karata je {BROJ_KARATA}.')
                broadcast(f'Preostalo je jos {BROJ_KARATA} karata!')
                print(len(clients))
            elif message.upper() == 'IZLAZ':
                print(f'{str(address)} se diskonektovao!')
                client.close()
                break
    except:
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

        
def auth(client, address):
    thread_dead = False
    client.send('Povezani ste sa serverom!'.encode(FORMAT))
    client.send('Izaberite neku od opcija\nlogin - za postojeci nalog\nregister - za registraciju\nizlaz - za izlaz iz aplikacije'.encode(FORMAT))

    message_recieved = client.recv(1024).decode(FORMAT)
    if message_recieved.lower() == 'login':
        client.send("Vase korisnicko ime: ".encode(FORMAT))
        username = client.recv(1024).decode(FORMAT)

        client.send("Vasa lozinka: ".encode(FORMAT))
        password = client.recv(1024).decode(FORMAT)

        check = login_provjera(username, password)
        if check == False:
            print("POGRESNI KREDENCIJALI")
            client.close()

    else:
        thread_dead = True
        client.send("Greska u unosu!")
        print(f'{str(address)} se diskonektovao!')
        client.close()
        return



    if thread_dead == False:
        recieve_thread = threading.Thread(target=recieve_choice, args=(client, address))
        recieve_thread.start()

def connection():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f'Uspjesno povezan sa {str(address)}')
        auth(client, address)
        #client.send('GREETINGPovezani ste sa serverom!\nIzaberite neku od opcija\nLIST - broj preostalih karata\nRESERVE - rezervisati kartu\nIZLAZ - za izlaz iz aplikacije'.encode(FORMAT))








print("Server is litening...")
# registracija_thread = threading.Thread(target=registracija)
# registracija_thread.start()
connection()





