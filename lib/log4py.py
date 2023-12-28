import datetime
import os


class Logger:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.log = []

    def custem(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{text}")
        print(self.log[len(self.log) - 1])

    def debug(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H:%M:%S')} DEBUG {text}")
        print(
            f"\033[95m{self.now.strftime('%Y-%m-%d %H:%M:%S')} \033[36mDEBUG\033[0m {text}"
        )

    def info(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H:%M:%S')} INFO {text}")
        print(
            f"\033[95m{self.now.strftime('%Y-%m-%d %H:%M:%S')} \033[94mINFO\033[0m \033[0m{text}"
        )

    def warning(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H:%M:%S')} WARNING {text}")
        print(
            f"\033[95m{self.now.strftime('%Y-%m-%d %H:%M:%S')} \033[33mWARNING\033[0m \033[0m{text}"
        )

    def error(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H:%M:%S')} ERROR {text}")
        print(
            f"\033[95m{self.now.strftime('%Y-%m-%d %H:%M:%S')} \033[91mERROR\033[0m \033[0m{text}"
        )

    def critical(self, text):
        self.now = datetime.datetime.now()
        self.log.append(f"{self.now.strftime('%Y-%m-%d %H:%M:%S')} CRITICAL {text}")
        print(
            f"\033[95m{self.now.strftime('%Y-%m-%d %H:%M:%S')} \033[31mCRITICAL\033[0m \033[0m{text}"
        )

    def save(self):
        self.now = datetime.datetime.now()
        os.chdir(os.getcwd())
        try:
            os.chdir(os.path.realpath("log"))
            f = open(
                f"{self.now.strftime('%Y-%m-%d %H-%M-%S')}.log", "w"
            )
            for i in self.log:
                f.write(f"{i}\n")
            f.close()
        except:
            os.mkdir(os.path.realpath("log"))
            os.chdir(os.path.realpath("log"))
            f = open(
                f"{self.now.strftime('%Y-%m-%d %H-%M-%S')}.log", "w"
            )
            for i in self.log:
                f.write(f"{i}\n")
            f.close()
        os.chdir(os.getcwd())
