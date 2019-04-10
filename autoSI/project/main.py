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
        self.headers = ""

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

    def genHeader(self):
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        accept_encoding = 'gzip,deflate,sdch'
        accept_language = 'zh-CN,zh;q=0.8'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

        self.headers = {
            'Accept' : accept,
            'Accept-Encoding' : accept_encoding,
            'Accept-Language' : accept_language,
            'User-Agent' : user_agent,
        }

    #login module
    def loginMethod(self):
        token = self.getLoginToken()
        if token != None:
            post_data = {
                'username' : self.userName,
                'password' : self.passWord,
                'authenticity_token' : token,
            }
            #login redmine
            #because redmine login success will redirect, so should forbidden it
            r = self.session.post(self.baseUrl + r'login', data=post_data, headers=headers, allow_redirects=False)

    #get token
    def getLoginToken(self):
        loginUrl = self.baseUrl + r'login'
        self.session = requests.Session()
        r = self.session.get(loginUrl, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup.find('input', {'name' : 'authenticity_token'})['value']
        '''for div in soup.find_all(id="login-form"):
            inputRslt = div.find_all("input")
            if inputRslt != None:
                for input in inputRslt:
                    name = input.get("name")
                    if name == "authenticity_token":
                        return input.get("value")'''

    #spider module
    def spiderMethod(self):
        roadmapUrl = self.baseUrl + r'projects/' + self.projectName.lower() + r'/roadmap'
        r = self.session.get(roadmapUrl)
        soup = BeautifulSoup(r.text, 'lxml')
        href = soup.find('a', {'name' : self.versionNumber})['href']
        latestSIUrl = r'http://192.168.100.103' + href

        #get all tickets information
        r = self.session.get(latestSIUrl)
        soup = BeautifulSoup(r.text, 'lxml')
        bugNumLst = list()
        for issue in soup.find_all('tr', {'class' : 'issue hascontextmenu'}):
            bugNumLst.append(issue.find('input')['value'])

        #enter into each tickets and get its information
        for bugNum in bugNumLst:
            url = self.baseUrl + r'issues/' + bugNum
            r = self.session.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            bugTtl = soup.find('div', {'class' : 'subject'}).find('h3').text
            bugSts = soup.find('div', {'class' : 'status attribute'}).find('div', {'class' : 'value'}).text
            bugPrssr = soup.find('div', {'class' : 'assigned-to attribute'}).find('a', {'class' : 'user active'}).text
            bugStrt = soup.find('div', {'class' : 'start-date attribute'}).find('div', {'class' : 'value'}).text
            bugPrgrss = soup.find('div', {'class' : 'progress attribute'}).find('p', {'class' : 'percent'}).text

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