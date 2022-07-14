from modulo_imap import*

def main():
    print("LOGIN".center(70, '-'))
    logado = login()
    while logado == False:
        login()
        logado = True
    
    numMensa = numeroTotalMensagens() #selecionando o inbox e pegando o número de mensagens
    
    while True:
        print("SELECIONE A OPÇÃO:".center(70,"_"))
        opcao = int(input("1-Ver E-mails    2-Ver Lixeira   3-Fazer Logout".center(69," ")))
        if opcao == 1:
            print("="*70)
            listarCabecalho(numMensa)
            print("-"*70)
            opcaoCabe = int(input("1-Abrir E-mail 2-Voltar: "))     
            while True:
                if opcaoCabe == 1:
                    abrirEmail(numMensa)
                    print("-"*70)
                    opcaoAberto = int(input("\n1-Responder 2-Voltar: "))
                    if opcaoAberto == 2:
                        break
                if opcaoCabe == 2:
                    break
        
        if  opcao == 3:
                logout()
                break

if __name__ == "__main__":
    main()