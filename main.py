import requests
import sqlite3
import threading

server_url = 'https://idiom.tingjieshaoer.cn/quiz1'
urser_token = '8f63e8a8cc594abe9b2ec8948dcad6be'


def log(type, status_code, elapsed):
    conn = sqlite3.connect('test_log.db', timeout=30000)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS log
                 (type TEXT,status_code INT,elapsed TEXT,time TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now','localtime')))''')

    cursor.execute('INSERT INTO log (type,status_code,elapsed) VALUES (?,?,?)',
                   (str(type), int(status_code), str(elapsed)))
    conn.commit()


def get_idioms():
    url = '{}/idioms.json/'.format(server_url)
    data = dict(user_token=urser_token, coin=10)
    sess = requests.Session()
    resp = sess.get(url, params=data)
    log('get_idiom', resp.status_code, resp.elapsed)


def get_rank():
    url = '{}/rank/'.format(server_url)
    data = dict(user_token=urser_token)
    sess = requests.Session()
    resp = sess.get(url, params=data)
    log('get_rank', resp.status_code, resp.elapsed)


def login():
    url = '{}/login/'.format(server_url)
    data = dict(user_token=urser_token)
    sess = requests.Session()
    resp = sess.get(url, params=data)
    log('login', resp.status_code, resp.elapsed)


def alter_coin():
    url = '{}/coin/'.format(server_url)
    data = dict(user_token=urser_token, coin=10)
    sess = requests.Session()
    resp = sess.post(url, json=data)
    log('alter_coin', resp.status_code, resp.elapsed)


def task():
    for i in range(0, 500):
        alter_coin()
        get_idioms()
        get_rank()
        get_idioms()
        alter_coin()
        login()


def do_in_thread():
    threads = [threading.Thread(target=task) for x in range(0, 30)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()


# do_in_thread()

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in environ.items()]
    return ret


# with make_server('', 8000, simple_app) as httpd:
#     print("Serving on port 8000...")
#     httpd.serve_forever()


class TestClass:
    qi = 'ol'
    sdfd = 'dfdsf'


# print(TestClass.qi)
# tc = TestClass()
# tc2 = TestClass()
#
# print(tc.sdfd)
# print(tc2.sdfd)
