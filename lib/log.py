import datetime
import os
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')
class log:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.log = []
    def debug(self,text):
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H-%M-%S')} - DEBUG - {text}")
        print(self.log[len(self.log)-1])
    def save(self):
        try:
            f = open(f"{os.getcwd()}\\log\\{self.now.strftime('%Y-%m-%d %H-%M-%S')}.log","w")
            for i in self.log:
                f.write(f"{i}\n")
            f.close
        except:
            os.mkdir("log")
            f = open(f"{os.getcwd()}\\log\\{self.now.strftime('%Y-%m-%d %H-%M-%S')}.log","w")
            for i in self.log:
                f.write(f"{i}\n")
            f.close
logs = log()
logs.debug("helo")
logs.debug("helo")
logs.save()