import requests
import curl
import wget
from bs4 import BeautifulSoup
import subprocess
import ctypes
import signal
import os
import json
libc = ctypes.CDLL("libc.so.6")


def set_pdeathsig(sig=signal.SIGTERM):
    def call_able():
        return libc.prctl(1, sig)
    return call_able

class Fshare:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.fshare = curl.Curl(base_url="https://www.fshare.vn")
        self.login_url = "site/login"
        self.download_url = "download/get"
        get_reponse = self.fshare.get(url=self.login_url).decode()
        self.fs_csrf = BeautifulSoup(get_reponse, 'html.parser').find("meta", attrs={'name': 'csrf-token'})\
            .get("content")
        self.isLogin = False

    def login(self):
        if self.isLogin is False:
            data_login = {'_csrf-app': self.fs_csrf,
                          'LoginForm[email]': self.email,
                          'LoginForm[password]': self.password,
                          'LoginForm[rememberMe]': 1}
            self.fshare.post(self.login_url, data_login).decode()

    def get_link(self, url):
        data_get = {'_csrf-app': self.fs_csrf,
                    'fcode5': '',
                    'linkcode': url.split('/')[-1],
                    'withFcode5': 0}
        # self.fshare.set_option(pycurl.FOLLOWLOCATION, 0)
        download_response = self.fshare.post(self.download_url, data_get).decode()
        link = json.loads(download_response.splitlines()[-1])['url']
        return link

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
            cmd = ['wget', '--restrict-file-names=nocontrol', '-nc', l]
            env = os.environ.copy()
            env['LD_LIBRARY_PATH'] = ''
            p = subprocess.Popen(cmd, shell=False, preexec_fn=set_pdeathsig(signal.SIGTERM), env=env)
            p.wait()
