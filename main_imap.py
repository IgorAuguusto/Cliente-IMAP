from modulo_imap import*

def main():
    print("LOGIN".center(70, '-'))
    logado = login()
    while logado == False:
        login()
        logado = True

    sistema_criacao_maillbox("TRASH")

    while True:
        print("SELECIONE A OPÇÃO:".center(70,"_"))
        opcao = int(input("1-Ver E-mails    2-Ver Lixeira   3-Fazer Logout".center(69," ")))
        if opcao == 1:
            sistema_de_inbox()
        else:
            if(opcao == 2):
                sistema_de_lixeira()
            else:
                if  opcao == 3:
                    logout()
                    break

def sistema_de_inbox():
    fecha_mailbox_atual()
    sistema_visualizacao_mailbox("INBOX",False)

def sistema_visualizacao_mailbox(nome_mailbox, is_lixeira):
    resposta_servidor = seleciona_mailbox(nome_mailbox)
    numero_mensagens = numeroTotalMensagens(resposta_servidor)
    lista_uids = uids(numero_mensagens)
    while True:
        print("="*70)
        print(" "*35 + nome_mailbox)
        print("="*70)
       
        listar_cabecalhos(lista_uids)
        print("-"*70) 
        opcao_escolhida = int(input("Escolha um e-mail para abrir ou -1 para voltar: "))
      
        if opcao_escolhida >=1 and opcao_escolhida < len(lista_uids):
            visualizar_email(lista_uids[opcao_escolhida -1][4])
            print("-"*70)
            opcao_aberto = int(input("\n1-Responder 2-Excluir 3-Voltar: "))
            if opcao_aberto == 2:
                if(not is_lixeira):
                    sistema_exclusao_email(lista_uids[opcao_escolhida -1][4])
                else:
                    sistema_exclusão_email_lixeira(lista_uids[opcao_escolhida -1][4])
                lista_uids = uids(numero_mensagens -1)
        else:
            if opcao_escolhida == -1:
                break
            print("\nNúmero de email inválido.")
        


def sistema_de_lixeira():
   sistema_visualizacao_mailbox("TRASH", True)





if __name__ == "__main__":
    main()