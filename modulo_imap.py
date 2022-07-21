from operator import index
import socket
import getpass
import re




#criando a conexão TCP com o servidor usando a porta do IMAP
serverName = "mail.labredes.info"
serverPort = 143
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((serverName, serverPort))
recv = tcp.recv(1024)
print(recv.decode('utf-8'))

if not "* OK" in recv.decode("utf-8"):
    print("Conexão Recusada")

#Realizando autenticação do usuário
def login(login,senha):
    login = login.split("@")
    tcp.send(f"1 LOGIN {login[0]} {senha}\r\n".encode())
    recv = (tcp.recv(1024))
    if recv[0:4].decode(('utf-8')) == ("1 OK"):
        print("Login Realizado com Sucesso\n")
        return True
    else:
        print("Falha ao logar")
        return False


def seleciona_mailbox(email_folder_name):
    tcp.send("2 SELECT {}\r\n".format(email_folder_name).encode())
    recv = (tcp.recv(1024))
    recv = recv.decode('utf-8').split("\r\n")
    return recv



#função que retorna o número total de mensagens existentes
def numero_total_mensagens(resposta_servidor):

    for i in range(0, len(resposta_servidor)):
        if "EXISTS" in resposta_servidor[i]:
            break
    
    if(i < len(resposta_servidor)):
        numbers_regex = re.compile(r'\d+(?:\.\d+)?')
        numero_mensagens = numbers_regex.findall(resposta_servidor[i])
        numero_mensagens = int(numero_mensagens[0]) #pegando o número total de mensagens 
        return numero_mensagens
    
    return 0

def fecha_mailbox_atual():
    tcp.send("30 close \r\n".encode())
    recv = (tcp.recv(1024))
    return "OK" in recv.decode(('utf-8'))
    


def verifica_existencia_mailbox(nome_folder):
    tcp.send("20 list \"\" \"*\" \r\n".encode())
    recv = (tcp.recv(1024))
    recv = recv.decode('utf-8').split("\r\n")
    for i in range(0, len(recv)):
        if(nome_folder in recv[i]):
            return True
    return False

def cria_mailbox(nome_folder):
    tcp.send("21 create {} \r\n".format(nome_folder).encode())
    recv = (tcp.recv(1024))
    return "OK" in recv.decode(('utf-8'))  


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



def listar_cabecalhos(uid):
    for cont in range(len(uid)-1):
        tcp.send(f"5 UID fetch {uid[cont][4]} (body[header.fields (from to subject date)])\r\n".encode())
        recv = tcp.recv(1024)
        recv = recv.decode("utf-8")
        recv = recv.split("\r\n")
        if  (uid[cont][6]) == "(\Seen" or (uid[cont][6]) == "(\Seen))":
            print(f"Email {uid[cont][1]} Visualizado".center(70, '_'))
        else:
            print(f"Email {uid[cont][1]} Não Visualizado".center(70, '_'))
        for i in range(1,5):
            print(recv[i])
    print()
    


def visualizar_email(email_uid):
    print()
    print("#"*70)
    print(f"EMAIL".center(70," "))
    print("#"*70)
    tcp.send(f"6 UID fetch {email_uid} (body[header.fields (from to subject date)])\r\n".encode())
    recv = tcp.recv(1024)
    recv = recv.decode("utf-8")
    lista = []
    recv = recv.split("\r\n")
    for i in range(len(recv)):
        if recv[i].startswith("From:") or recv[i].startswith("from:"):
            lista.append(recv[i])
        elif  recv[i].startswith("Subject:") or recv[i].startswith("subject:"):
            lista.append(recv[i])
        elif recv[i].startswith("To:") or recv[i].startswith("to:"):
            lista.append(recv[i])
        elif recv[i].startswith("Date:") or recv[i].startswith("date:"):
            lista.append(recv[i])
    print()
    for i in range(len(lista)):
        print(lista[i])
    print()
    tcp.send(f"30 UID fetch {email_uid} body[text] \r\n".encode())
    recv = tcp.recv(40000)
    recv = recv.decode("utf-8")
    recv = recv.split("\r\n")
    del recv[0],recv[-3:-1]
    for i in range(len(recv)):
        print(recv[i])
    

def destinatario_assunto(uid):
    tcp.send(f"6 UID fetch {uid} (body[header.fields (from to subject date)])\r\n".encode())
    recv = tcp.recv(1024)
    recv = recv.decode("utf-8")
    
    recv = recv.split("\r\n")
    for i in range(len(recv)):
        if recv[i].startswith("From:") or recv[i].startswith("from:"):
            destinatario = recv[i]
    
        elif  recv[i].startswith("Subject:") or recv[i].startswith("subject:"):
            assunto = recv[i]

    if "<" in destinatario:
        destinatario = destinatario.split("<")
        destinatario = destinatario[1].split(">")
        destinatario = destinatario[0]
    else:
        destinatario = destinatario.split(":")
        destinatario = destinatario[1]

    if "Subject:" in assunto or "subject:" in assunto:
        assunto = assunto.split(":")
    
    return destinatario, assunto[1]
     

def sistema_exclusao_email(email_uid):
    if(copiar_email_para_outra_mailbox(email_uid, "TRASH")):
        print("\nEmail movido para a lixeira\n")
    if(marcar_email_para_exclusao(email_uid)):
        print("\nEmail maracado para ser excluido\n")
    if(executa_comando_expunge()):
        print("\nEmail excluido\n")
    

def sistema_exclusão_email_lixeira(email_uid):
    marcar_email_para_exclusao(email_uid)
    executa_comando_expunge()


def executa_comando_expunge():
    tcp.send("24 expunge\r\n".encode())
    recv = tcp.recv(1024)
    return "OK" in recv.decode(('utf-8'))  

def marcar_email_para_exclusao(email_uid):
    tcp.send("23 uid store {} +flags.silent (\Seen \Deleted)\r\n".format(email_uid).encode())
    recv = tcp.recv(1024)
    return "OK" in recv.decode(('utf-8'))  

def copiar_email_para_outra_mailbox(email_uid, mailbox_name):
    tcp.send("22 uid copy {} {}\r\n".format(email_uid, mailbox_name).encode())
    recv = tcp.recv(1024)
    return "OK" in recv.decode(('utf-8'))  
        


    
def sistema_criacao_maillbox(mailbox_name):
    fecha_mailbox_atual()
    if(not verifica_existencia_mailbox(mailbox_name)):
        if(cria_mailbox(mailbox_name)):
            print("{} criado".format(mailbox_name))
    


#Realizando Logout 
def logout():

    tcp.send("9 LOGOUT\r\n".encode("utf-8"))
    recv = (tcp.recv(1024))
    if recv[:5].decode(("utf-8")) == ("* BYE"):
        print("\nLogout Feito com sucesso !!\n")
    else:
        print("\nFalha ao sair do servidor\n")
    tcp.close() #Fechando a conexão com o servidor
