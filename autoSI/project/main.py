import os
import configparser
import urllib3
import bs4

class AutoSI(object):
    def __init__(self):
        self.userName = ""
        self.passWord = ""
        self.versionNumber = ""
        self.projectName = ""
        self.url = ""

    def getConfigPath(self):
        return os.getcwd() + r"\config.ini"

    #config module
    def configMethod(self, fileName):
        config = configparser.ConfigParser()
        config.read(fileName)
        self.userName = config.get("RedmineInfo", "username")
        self.passWord = config.get("RedmineInfo", "password")
        self.versionNumber = config.get("ProjectInfo", "version")
        self.projectName = config.get("ProjectInfo", "projname")
        self.url = config.get("RedmineInfo", "url")

    #login module
    def loginMethod(self):
        pass

    #spider module
    def spiderMethod(self):
        pass

    #compile module
    def compileMethod(self):
        pass

    #message module
    def notifyMethod(self):
        pass

    #data analysis module
    def analysisMethod(self):
        pass

if __name__ == "__main__":
    obj = AutoSI()
    cfg = obj.getConfigPath()
    obj.configMethod(cfg)