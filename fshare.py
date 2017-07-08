import json
import requests
import curl
import re
from lxml import html
import pycurl


class Fshare:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.fshare = curl.Curl(base_url="https://www.fshare.vn")
        self.login_url = "login"
        self.download_url = "download/get"
        get_reponse = self.fshare.get(url=self.login_url).decode()
        self.fs_csrf = re.findall(r'(\b[a-f0-9]+\b)(?=" name="fs_csrf")', get_reponse)[0]
        self.isLogin = False

    def login(self):
        if self.isLogin is False:
            data_login = {'fs_csrf': self.fs_csrf,
                          'LoginForm[email]': self.email,
                          'LoginForm[password]': self.password,
                          'LoginForm[rememberMe]': 1,
                          'LoginForm[checkloginpopup]': 0,
                          'yt0': u'Đăng nhập'}
            login_reponse = self.fshare.post(self.login_url, data_login).decode()
            # print("HEADER")
            # print(self.fshare.header())
            # print("INFO")
            # print(self.fshare.info())

    def get_link(self, url):
        self.fshare.set_option(pycurl.FOLLOWLOCATION, 0)
        self.fshare.get(url=url).decode()
        return re.findall(r'(Location:)(.*)', self.fshare.header())[0][1].strip()

