import socket
import base64

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
else:
    print('\nConexão estabelecida')



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
        return 0
    else:
        return 1



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
    message = 'from:' + from_address + '@labredes.info' + '\r\n'
    message += 'to:' + to_address + '\r\n'
    message += 'subject:' + subject + '\r\n'
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

    tcp.sendall('QUIT\r\n'.encode())



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
    message = 'from:' + from_address + '@labredes.info' + '\r\n'
    message += 'to:' + to_address + '\r\n'
    message += 'subject:' +  "Re: " + subject + '\r\n'
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

    tcp.sendall('QUIT\r\n'.encode())
