#!/usr/bin/env python
from fshare import Fshare
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wget
import json
import os


def main():
    with open(os.path.join(os.path.dirname(__file__), 'acc_info.json'), 'r') as fp:
        # global acc_info
        acc_info = json.load(fp=fp)

    fshare = Fshare(email=acc_info['email'], password=acc_info['pass'])
    fshare.login()
    list_argv = sys.argv
    if len(list_argv) > 1:
        for link in list_argv[1::]:
            if link.find('fshare.vn/file') >= 0:
                # print(fshare.get_link(link))
                wget.download(fshare.get_link(link))
            else:
                fshare.get_folder(link)


if __name__ == '__main__':
    main()



