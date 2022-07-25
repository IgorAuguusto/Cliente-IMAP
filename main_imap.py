
from modulo_imap import*
from modulo_smtp import login_sm, enviar_email, responder_email, logout_stmp

def main():
    global email
    print("LOGIN".center(70, '-'))
    email = input("Entre com seu e-mail: ")
    senha = getpass.getpass(prompt='Password: ', stream=None)
    teste_login_imap = login(email,senha)
    teste_login_smtp = login_sm(email,senha)

    while not teste_login_imap and not teste_login_smtp:
        print("LOGIN".center(70, '-'))
        email = input("Entre com seu e-mail: ")
        senha = getpass.getpass(prompt='Password: ', stream=None)
        teste_login_imap = login(email,senha)
        teste_login_smtp = login_sm(email,senha)

    
    sistema_criacao_maillbox("TRASH")

    while True:
        print("SELECIONE A OPÇÃO:".center(70,"_"))
        opcao = int(input("1-Ver E-mails    2-Ver Lixeira   3-Enviar E-mail    4-Fazer Logout".center(69," ")))
        if opcao == 1:
            sistema_de_inbox()
        else:
            if(opcao == 2):
                sistema_de_lixeira()
            else:
                if  opcao == 3:
                    enviar_email(email)
                else:
                    if opcao == 4:
                        logout()
                        logout_stmp()
                        break

def sistema_de_inbox():
    fecha_mailbox_atual()
    sistema_visualizacao_mailbox("INBOX",False)

def sistema_visualizacao_mailbox(nome_mailbox, is_lixeira):
    while True:
        resposta_servidor = seleciona_mailbox(nome_mailbox)
        numero_mensagens = numero_total_mensagens(resposta_servidor)
        lista_uids = uids(numero_mensagens)
        print("="*70)
        print(f"{nome_mailbox}".center(70," "))
        print("="*70)
       
        listar_cabecalhos(lista_uids)
        print("-"*70) 
        opcao_escolhida = int(input("Escolha um e-mail para abrir ou -1 para voltar: "))
      
        if opcao_escolhida >=1 and opcao_escolhida < len(lista_uids):
            visualizar_email(lista_uids[opcao_escolhida -1][4])
            print("#"*70)
            opcao_aberto = int(input("\n1-Responder 2-Excluir 3-Voltar: "))
            if opcao_aberto == 1:
                destinatario , assunto = destinatario_assunto(lista_uids[opcao_escolhida -1][4])
                responder_email(email,destinatario,assunto)
                break

            if opcao_aberto == 2:
                if(not is_lixeira):
                    sistema_exclusao_email(lista_uids[opcao_escolhida -1][4])
                else:
                    sistema_exclusão_email_lixeira(lista_uids[opcao_escolhida -1][4])
                lista_uids = uids(numero_mensagens -1)
            if opcao_aberto == 3:
                continue
        else:
            if opcao_escolhida == -1:
                break
            print("\nNúmero de email inválido.")
        


def sistema_de_lixeira():
   sistema_visualizacao_mailbox("TRASH", True)





if __name__ == "__main__":
    main()