import socket


#criando a conexão TCP com o servidor usando a porta do IMAP
serverName = "mail.labredes.info"
serverPort = 143
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((serverName, serverPort))
recv = tcp.recv(1024)
print(recv.decode('utf-8'))

if "* OK" in recv.decode("utf-8"):
    print("Conexão estabelecida")
else:
    print("Conexão Recusada")

#Realizando autenticação do usuário
def login():

    login = input("Entre com seu e-mail: ")
    senha = input("Entre com a sua senha: ")
    login = login.split("@")
    tcp.send(f"1 LOGIN {login[0]} {senha}\r\n".encode("utf-8"))
    recv = (tcp.recv(1024))
    if recv[0:4].decode(('utf-8')) == ("1 OK"):
        print("Login Realizado com Sucesso\n")
    else:
        print("Falha ao logar")


#função que retorna o número total de mensagens existentes
def numeroTotalMensagens():
    tcp.send("2 SELECT inbox\r\n".encode("utf-8"))
    recv = (tcp.recv(1024))
    recv = recv.decode('utf-8').split("\r\n")
    numeroMesangens = recv[2]
    numeroMesangens = list(numeroMesangens)
    numeroMesangens = int(numeroMesangens[2]) #pegando o número total de mensagens 
    return numeroMesangens;

#função que cria uma matriz com os uids, flags e status das mensagem
def uids(tamanho): 
    tcp.send("4 UID fetch 1:* (FLAGS)\r\n".encode())
    recv = tcp.recv(2048)
    recv = recv.decode('utf-8')
    recv = recv.split("\r\n")
    
    for i in range(tamanho):
        recv[i] = recv[i].split(" ") #criando uma matriz com a resposta do servidor [x][4] = coluna 4 guarda o uid e [x][1] e o numero do email 
    
    del recv[-1]
    
    if "OK" in recv[-1]:
        return recv
    else:
        print("UID FETCH FALHOU")

#
def listarCabecalho(tamanho):    
    uid = uids(tamanho)
    for cont in range(len(uid)-1):
        tcp.send(f"5 UID fetch {uid[cont][4]} (body[header.fields (from to subject date)])\r\n".encode())
        recv = tcp.recv(2048)
        recv = recv.decode("utf-8")
        recv = recv.split("\r\n")
        print(f"Email {uid[cont][1]}".center(50, '_'))
        for i in range(1,5):
            print(recv[i])
    print()

def abrirEmail(tamanho):
    uid = uids(tamanho)
    numeroDoEmail = input("Forneça o número do email que deseja abrir: ")
    for cont in range(len(uid)):
        if numeroDoEmail == uid[cont][1]:
            tcp.send(f"6 UID fetch {uid[cont][4]} (UID RFC822.SIZE BODY.PEEK[])\r\n".encode())
            #tcp.send(f"6 fetch {uid[cont][4]} body[text]\r\n".encode())
            recv = tcp.recv(1024)
            recv = recv.decode("utf-8")
            return print("\n",recv)
    print("Número que corresponde ao email não foi encontrado")  
    return abrirEmail(tamanho)

    



#Realizando Logout 
def logout():

    tcp.send("9 LOGOUT\r\n".encode("utf-8"))
    recv = (tcp.recv(1024))
    if recv[:5].decode(("utf-8")) == ("* BYE"):
        print(recv.decode("utf-8"))
        print("Logout Feito com sucesso !!")
    else:
        print("Falha ao sair do servidor\n")
        print(recv)
    tcp.close() #Fechando a conexão com o servidor


teste = 1

while teste: 
    t = int(input("Forneca 1-para logar e 2-para sair 3-E-mails: ")) 

    if t == 1:
        login()
        tamanho = numeroTotalMensagens()
    if t == 3:

        listarCabecalho(tamanho)
        abrirEmail(tamanho)


    if t == 2:
        logout()
        teste = 0

# if __name__ == "__main__":