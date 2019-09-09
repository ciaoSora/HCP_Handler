import requests
import hashlib
import json

# Global constant
LOGIN_URL = "http://172.18.160.21/stage/v2/login"
HOME_URL  = "http://172.18.160.21/stage/v2/homework-dashboard"
session = requests.Session()
NORMAL_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           }
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Content-Type": "application/json;charset=UTF-8",
           }


# Return TRUE if login successfully
# In fact, one can perform any operation on the MA without necessarilly login
def login(username, password):
    username = str(username)
    password = str(password)
    part1 = 'http://172.18.160.21/stage/v2/api/Customers?filter={"where":{"username":"'
    part2 = '","password":"'
    part3 = '"}}'
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    url = part1 + username + part2 + password + part3
    r = session.get(url, headers = NORMAL_HEADERS)
    return r.text != "[]"

# Return a list of corresponding users
# type(info) can one of the following three:
#     1. dict   for user detailed info
#     2. int    for student ID
#     3. str    for student ID
def get_user(info):
    if type(info) == int:
        info = '{"username": "' + str(info) + '"}'
    elif type(info) == str:
        info = '{"username": "' + info + '"}'
    elif type(info) == dict:
        info = str(info).replace("'", '"')
    else:
        return "invalid param"
    part1 = 'http://172.18.160.21/stage/v2/api/Customers?filter={"where":'
    part2 = '}'
    url = part1 + info + part2
    r = session.get(url, headers = NORMAL_HEADERS)
    return json.loads(r.text)

# Return a list of reviewers or revierees of username
# param = 0 for reviewee, otherwise for reviewer
def check(param, username, homeworkid):
    if type(param) == int:
        if param == 0:
            param = 'e'
        else:
            param = 'r'
    part1 = 'http://hcp.sysu.edu.cn/stage/v2/api/Reviews?filter={"where":{"reviewe'
    part2 = '.username":"'
    part3 = '","homeworkId":'
    part4 = '}}'
    username = str(username)
    homeworkid = str(homeworkid)
    url = part1 + param + part2 + username + part3 + homeworkid + part4
    r = session.get(url, headers = NORMAL_HEADERS)
    return json.loads(r.text)
