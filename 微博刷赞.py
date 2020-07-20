import re
import rsa
import time
import json
import string
import base64
import random
import binascii
import requests
import threading
import urllib.parse
from lxml import etree

# zhanghao = '1548533264@qq.com'
# mima = 'qingtian33..'


class Weibo():

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"})
        self.session.get("http://weibo.com/login.php")
        self.session.proxies = {
            "http": "http://27.50.151.240:28803",
            "https": "http://27.50.151.240:28803",
        }
    # 加密用户名

    def get_username(self):
        username_quote = urllib.parse.quote_plus(zhanghao)
        self.username_base64 = base64.b64encode(
            username_quote.encode("utf-8")).decode("utf-8")
    # 获取json重要

    def get_json_data(self):
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": self.username_base64,
            "_": int(time.time() * 1000),
        }
        try:
            response = self.session.get(
                "http://login.sina.com.cn/sso/prelogin.php", params=params)
            self.json_data = json.loads(
                re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except:
            pass
    # 加密密码

    def get_password(self):
        string = (str(self.json_data["servertime"]) + "\t" + str(self.json_data["nonce"]) + "\n" + str(mima)).encode(
            "utf-8")
        public_key = rsa.PublicKey(
            int(self.json_data["pubkey"], 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        self.password = binascii.b2a_hex(password).decode()
    # 获取验证码

    def yzm(self):
        if self.json_data["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (
                int(time.time()), self.json_data["pcid"])
            # print('请点击此网站查看验证码\n' + url)
            r = self.session.get(url)
            with open("验证码.jpeg", "wb") as fp:
                fp.write(r.content)
            weibo.main('',
                       '',
                       '验证码.jpeg',
                       "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload",
                       '1',
                       '8',
                       '1001',
                       '')
        else:
            self.code = ''
    # 开始登录

    def main(self, api_username, api_password, file_name, api_post_url, yzm_min, yzm_max, yzm_type, tools_token):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
            'Connection': 'keep-alive',
            'Host': 'v1-http-api.jsdama.com',
            'Upgrade-Insecure-Requests': '1'
        }

        files = {
            'upload': (file_name, open(file_name, 'rb'), 'image/png')
        }

        data = {
            'user_name': api_username,
            'user_pw': api_password,
            'yzm_minlen': yzm_min,
            'yzm_maxlen': yzm_max,
            'yzmtype_mark': yzm_type,
            'zztool_token': tools_token
        }
        s = requests.session()
        # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
        r = s.post(api_post_url, headers=headers,
                   data=data, files=files, verify=False)
        self.code = r.json()['data']['val']
        # print(self.code)
    # 开始登录

    def login_pc(self):
        weibo.get_username()
        weibo.get_json_data()
        weibo.get_password()
        weibo.yzm()
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": self.json_data["rsakv"],
            "servertime": self.json_data["servertime"],
            "nonce": self.json_data["nonce"],
            "su": self.username_base64,
            "sp": self.password,
            "returntype": "TEXT",
        }
        # self.code = input('asd')
        post_data["pcid"] = self.json_data["pcid"]
        post_data["door"] = self.code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(
            time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time() * 1000),
            }
            response = self.session.get(
                "https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(
                re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                print('电脑网页版本登录成功\n此账号的id为：' + str(self.user_uniqueid) +
                      '\n' + '此账号的名字为：' + self.user_nick)
                with open('可以的登录的账号.txt', 'a') as pt:
                    pt.write(str(zhanghao)+'----'+str(mima)+'\n')
                weibo.zan()
            else:
                print('账号密码错误')
        else:
            print('验证码错误,重新登录')
            try:
                weibo.login_pc1()
            except:
                pass

    def zan(self):
        ts = int(time.time()*1000)
        url = 'https://weibo.com/aj/v6/like/objectlike?ajwvr=6&__rnd={}'.format(
            ts)
        data = {
            'location': 'page_100505_single_weibo',
            'object_id': object_id,
            'object_type': 'comment',
            'o_uid': o_uid,
            'commentmid': commentmid,
            'floating': '0',
            '_t': '0',
        }
        headers = {
            'Host': 'weibo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '0',
            'Origin': 'https://weibo.com',
            'Connection': 'keep-alive',
            'Referer': 'https://weibo.com/{}/IFAbBaq4g?type=comment'.format(uid_taren),
            'TE': 'Trailers',
        }
        res = self.session.post(url, headers=headers, data=data)
        # print(res.json())
        if int(res.json()['code']) == 100000:
            print('点赞成功')
        else:
            print('点赞失败'+'\t'+'原因:'+str(res.json()['msg']))

    def login_pc1(self):
        weibo.get_username()
        weibo.get_json_data()
        weibo.get_password()
        weibo.yzm()
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": self.json_data["rsakv"],
            "servertime": self.json_data["servertime"],
            "nonce": self.json_data["nonce"],
            "su": self.username_base64,
            "sp": self.password,
            "returntype": "TEXT",
        }
        # self.code = input('asd')
        post_data["pcid"] = self.json_data["pcid"]
        post_data["door"] = self.code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(
            time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time() * 1000),
            }
            response = self.session.get(
                "https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(
                re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                print('电脑网页版本登录成功\n此账号的id为：' + str(self.user_uniqueid) +
                      '\n' + '此账号的名字为：' + self.user_nick)
                with open('可以的登录的账号.txt', 'a') as pt:
                    pt.write(str(zhanghao)+'----'+str(mima)+'\n')
                weibo.zan()
            else:
                print('账号密码错误')
        else:
            print('验证码错误,重新登录')


if __name__ == "__main__":
    uid_taren = input('请输入文章用户的ID')
    object_id = input('请输入object_id')
    o_uid = input('请输入o_uid')
    commentmid = input('请输入commentmid')
    with open('1.txt', encoding='utf-8') as fp:
        dd = fp.readlines()
        for line in dd:
            line = line.strip("\n")
            zhanghao = re.findall('(.*?)----.*?----.*?', line)[0]
            mima = re.findall('.*?----(.*?)----.*?', line)[0]
            print(zhanghao, mima)
            weibo = Weibo()
            try:
                weibo.login_pc()
            except:
                pass
