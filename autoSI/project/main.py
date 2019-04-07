import os
import configparser
import requests
from bs4 import BeautifulSoup
import re
import git

class AutoSI(object):
    def __init__(self):
        self.userName = ""
        self.passWord = ""
        self.versionNumber = ""
        self.projectName = ""
        self.baseUrl = ""
        self.basepath = ""
        self.targetpath = ""
        self.gitrepo = ""
        self.session = ""

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
        self.baseUrl = config.get("RedmineInfo", "baseurl")
        self.basepath = config.get("CompileInfo", "basepath")
        self.targetpath = config.get("CompileInfo", "targetpath")
        self.gitrepo = config.get("CompileInfo", "gitrepo")

    #login module
    def loginMethod(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        token = self.getLoginToken()
        if token != None:
            headers = {
                'User-Agent' : user_agent,
                'username' : self.userName,
                'password' : self.passWord,
                'authenticity_token' : token
            }
            #login redmine
            r = self.session.get(self.baseUrl + r'login', headers=headers)

    #get token
    def getLoginToken(self):
        loginUrl = self.baseUrl + r'login'
        self.session = requests.Session()
        r = self.session.get(loginUrl)
        soup = BeautifulSoup(r.text, 'lxml')
        for div in soup.find_all(id="login-form"):
            inputRslt = div.find_all("input")
            if inputRslt != None:
                for input in inputRslt:
                    name = input.get("name")
                    if name == "authenticity_token":
                        return input.get("value")

    #spider module
    def spiderMethod(self):
        projectUrl = self.baseUrl + r'projects/' + self.projectName
        print(projectUrl)
        r = self.session.get(projectUrl)
        print(r.text)

    def getLatestCodeOfGit(self):
        localCodePath = self.targetpath.replace("<version>", self.versionNumber)
        git.Repo.clone_from(self.gitrepo, localCodePath)

    #compile module
    def compileMethod(self):
        self.getLatestCodeOfGit()
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
    obj.loginMethod()
    obj.spiderMethod()