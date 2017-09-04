import json
import requests
import curl
import re
from lxml import html, etree
import pycurl
from bs4 import BeautifulSoup
import subprocess
import glob
import ctypes
libc = ctypes.CDLL("libc.so.6")
import signal
import os

def set_pdeathsig(sig = signal.SIGTERM):
    def callable():
        return libc.prctl(1, sig)
    return callable


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

    def get_folder_info(self, url):
        page = requests.get(url)
        h = BeautifulSoup(page.content, 'html.parser')
        result = list()
        for l in h.find_all(class_='filename', href=True, title=True):
            if l.text.strip():
                result.append((l['href'], l['title']))

        return result

    def get_folder(self, url):
        link_list = self.get_folder_info(url)
        for link in link_list:
            l = self.get_link(link[0])
            print(l)
            print(link[1])
            cmd = ['wget', '--restrict-file-names=nocontrol', l]
            env = os.environ.copy()
            env['LD_LIBRARY_PATH'] = ''
            p = subprocess.Popen(cmd, shell=False, preexec_fn=set_pdeathsig(signal.SIGTERM), env=env)
            p.wait()




# my_fshare = Fshare("generaltrung2@gmail.com", "!199485623")
# my_fshare.get_folder("https://www.fshare.vn/folder/TS45W71JMT")

