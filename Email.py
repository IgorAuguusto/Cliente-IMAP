class Email:

    def __init__(self, uID, headder, body, read):
        self.uID = uID
        self.headder = headder
        self.body = body
        self.wasRead = read
        
    def GetUID(self):
        return self.uID

    def GetHeadder(self):
        return self.headder

    def GetBody(self):
        return self.body

    def GetWasRead(self):
        return self.wasRead

    def ToString(self):
        return "UID {0}\n{1}\n{2}\nStatus {3}".format(self.uID, self.headder, self.body, self.wasRead)



    




        




   