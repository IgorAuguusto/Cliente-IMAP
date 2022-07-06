from operator import le
from Email import Email

CANCEL_OPTION = -1

class EmailManager:

    def __init__(self):
        self.emailList = []
        pass

    def AddEmail(self, newEmail):
        self.emailList.append(newEmail)
    
    def DeleteEmail(self, whichEmail):
        ##Colocar aqui o método para remover um email do servidor
        self.emailList.remove(whichEmail)
    
    def ListEmailsHeadders(self):
        index = 0
        for email in self.emailList:
            print("{0} {1}\n".format(index, email.headder))
            index +=1
    
    def ShowEmailBody(self, whichEmail):
        if(whichEmail < len(self.emailList)):
            print("\nEmail Body:" + self.emailList[whichEmail].body + "\n")
            self.emailList[whichEmail].wasRead = True
            ## Colocar aqui o método para falar para o servidor que o email com essa UID foi lido

    def EmailInboxSystem(self):
       choice = 0
       while choice != -1: 
        choice = self.UserChoiceValidationSystem()
        if(choice != -1):
            self.ShowEmailBody(choice)
        

    def UserChoiceValidation(self, choice, minimumValue, maximumValue):
        if(choice.isnumeric()):
            choice = int(choice)
            return -(choice >= minimumValue and choice < maximumValue)
        return False
    
    def CancelOption(self, choice):
        return int(choice) == CANCEL_OPTION

    def UserChoiceValidationSystem(self):
        choice = -1
        while True:
            self.ListEmailsHeadders()
            print("Escolha um email informando o número do mesmo(-1 para sair):")
            choice = input("Opção:")
            if(self.UserChoiceValidation(choice,0, len(self.emailList)) or self.CancelOption(choice)):
                break
            else:
                print("Número de email inválido")
        return int(choice)

            
        

    

        
manager = EmailManager()

manager.AddEmail(Email(0,"Teste","TesteBody", False))
manager.AddEmail(Email(1,"Teste2","TesteBody2", True))


manager.EmailInboxSystem()