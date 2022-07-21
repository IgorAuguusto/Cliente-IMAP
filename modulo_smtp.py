import socket
import base64
import time

#Criando a conexão TCP com o servidor usando a porta do SMTP
server_name = "mail.labredes.info"
server_port = 587
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((server_name, server_port))
recv = tcp.recv(1024)

recv = recv.decode()

if recv[:3] != '220':
    print('\nResposta não recebida pelo servidor.')

#Executando o comando Helo para estabelecer uma conexão SMTP com o servidor
helo_command = 'HELO Lab\r\n'
tcp.send(helo_command.encode())
recv = tcp.recv(1024)
recv = recv.decode()
\
if recv[:3] != '250':
    print('\nResposta não recebida pelo servidor.')

#função que retorna uma mensagem com a data atual
def tempo():

    timestamp = time.time()  
    timeArray = time.localtime(timestamp) 
    formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) 
    formatar = formatTime.split('-')

    if formatTime[5:7] == '01':
        mes = 'Jan'
    elif formatTime[5:7] == '02':
        mes = 'Feb'
    elif formatTime[5:7] == '03':
        mes = 'Mar'
    elif formatTime[5:7] == '04':
        mes = 'Apr'
    elif formatTime[5:7] == '05':
        mes = 'May'
    elif formatTime[5:7] == '06':
        mes = 'Jun'
    elif formatTime[5:7] == '07':
        mes = 'Jul'
    elif formatTime[5:7] == '08':
        mes = 'Aug'
    elif formatTime[5:7] == '09':
        mes = 'Sep'
    elif formatTime[5:7] == '10':
        mes = 'Oct'
    elif formatTime[5:7] == '11':
        mes = 'Nov'
    else:
        mes = 'Dec'

    return (f'Date: Fri, {formatTime[8:10]} {mes} {formatTime[0:4]} {formatTime[11:19]} -0300\r\n')


#Realizando autenticação do usuário
def login_sm(username,password):

    base64_str = ("\x00"+username+"\x00"+password).encode()
    base64_str = base64.b64encode(base64_str)
    auth_msg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    tcp.send(auth_msg)
    recv_auth = tcp.recv(1024)

    recv = (recv_auth.decode())

#Se o valor de retorno de "recv" for diferente de 235 a autenticação falhou
    if (recv[:3] != '235'):
        return False
    else:
        return True



#Função para enviar o e-mail
def enviar_email(username):

    content_type = "text/plain" #informando para o servidor que o conteúdo se trata de um texto simples
    from_address = username
    to_address = input('\nDigite o destinatário: ')
    subject = input('\nDigite o assunto: ')
    msg = input('\nDigite a mensagem: ')
    end_msg = "\r\n.\r\n"

    
    # Enviando o comando MAIL FROM e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('MAIL FROM: <'+from_address+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')
    

    # Enviando o comando RCPT e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('RCPT TO: <'+to_address+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')


    # Enviando o comando DATA e imprimindo a resposta do servidor casou houver erro.
    tcp.send(('DATA\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '354'):
        print('Resposta não recebida do servidor')


    #Enviando dados da mensagem para o destinatário
    data = tempo()
    message = 'Subject:' + subject + '\r\n'
    message += 'From:' + from_address + '@labredes.info' + '\r\n'
    message += 'To:' + to_address + '\r\n'
    message +=data
    message += 'Content-Type:' + content_type + '\r\n'
    message += '\r\n' + msg
    tcp.sendall(message.encode())


    #Informando o fim da mensagem para o servidor e imprimindo a resposta caso houver erro
    tcp.sendall(end_msg.encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('Resposta não recebida do servidor')
    else:
        print('\nMensagem enviada com sucesso!\n')

   


#Função para enviar o e-mail
def responder_email(username, destinatario, assunto):

    content_type = "text/plain" #informando para o servidor que o conteúdo se trata de um texto simples
    from_address = username
    to_address = destinatario
    subject = assunto
    msg = input('\nDigite a mensagem: ')
    end_msg = "\r\n.\r\n"

    
    # Enviando o comando MAIL FROM e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('MAIL FROM: <'+from_address+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')
    

    # Enviando o comando RCPT e imprimindo a resposta do servidor casou houver erro.
    tcp.sendall(('RCPT TO: <'+to_address+'>\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('\nResposta não recebida do servidor.')


    # Enviando o comando DATA e imprimindo a resposta do servidor casou houver erro.
    tcp.send(('DATA\r\n').encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '354'):
        print('Resposta não recebida do servidor')


    #Enviando dados da mensagem para o destinatário
    data = tempo()
    message = 'Subject:' + subject + '\r\n'
    message += 'From:' + from_address + '@labredes.info' + '\r\n'
    message += 'To:' + to_address + '\r\n'
    message +=data
    message += 'Content-Type:' + content_type + '\r\n'
    message += '\r\n' + msg
    tcp.sendall(message.encode())


    #Informando o fim da mensagem para o servidor e imprimindo a resposta caso houver erro
    tcp.sendall(end_msg.encode())
    recv = tcp.recv(1024).decode()
    if (recv[:3] != '250'):
        print('Resposta não recebida do servidor')
    else:
        print('\nMensagem enviada com sucesso!\n')

    


def logout_stmp():
    tcp.sendall('QUIT\r\n'.encode())
    tcp.close()

