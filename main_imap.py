from modulo_imap import*

def main():
    print("LOGIN".center(70, '-'))
    logado = login()
    while logado == False:
        login()
        logado = True

    #selecionando o inbox
    resposta_servidor = seleciona_mailbox("INBOX")

    #pegando o número de mensagens
    numMensa = numeroTotalMensagens(resposta_servidor) 
    while True:
        print("SELECIONE A OPÇÃO:".center(70,"_"))
        opcao = int(input("1-Ver E-mails    2-Ver Lixeira   3-Fazer Logout".center(69," ")))
        if opcao == 1:
            sistema_visualizacao_mailbox("INBOX")

        else:
            if(opcao == 2):
                sistema_de_lixeira()
            else:
                if  opcao == 3:
                    logout()
                    break


def sistema_visualizacao_mailbox(nome_mailbox):
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
            # if opcao_aberto == 3:
            #     break
        else:
            if opcao_escolhida == -1:
                break
            print("\nNúmero de email inválido.")
        


def sistema_de_lixeira():
    ##visualizar_lixeira()
    if(not verifica_existencia_mailbox("TRASH")):
        if(cria_mailbox("TRASH")):
            print("Lixeira criada.".center(75," "))
   
    sistema_visualizacao_mailbox("TRASH")





if __name__ == "__main__":
    main()