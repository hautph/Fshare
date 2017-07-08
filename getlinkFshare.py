from fshare import Fshare
import sys
import json


def main():
    with open('acc_info.json', 'r') as fp:
        # global acc_info
        acc_info = json.load(fp=fp)

    fshare = Fshare(email=acc_info['email'], password=acc_info['pass'])
    fshare.login()
    list_argv = sys.argv
    if len(list_argv) > 1:
        for link in list_argv[1::]:
            print(fshare.get_link(link))


if __name__ == '__main__':
    main()



