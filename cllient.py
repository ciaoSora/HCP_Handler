from kernel import check
import sqlite3

conn = sqlite3.connect("user.db")
c = conn.cursor()

def toUsername(target):
    condition = ""
    if target.isnumeric():
        condition = "USERNAME = '" + target + "'"
    elif target.encode("UTF-8").isalpha() and len(target) < 5:
        condition = "PINYIN = '" + target.lower() + "'"
    else:
        condition = "FULLNAME = '" + target + "'"
    s = "SELECT USERNAME, FULLNAME FROM USER WHERE " + condition
    cursor = c.execute(s)
    target = []
    for row in cursor:
        target.append(row)
    return target
    
homeworkid = input("欢迎！请输入目标作业ID（第一次作业ID就是1，以此类推）：")
while not homeworkid.isnumeric():
    homeworkid = input("请输入合法作业ID：")
while True:
    target = input("请输入目标姓名、或学号、或拼音首字母缩写：")
    target = toUsername(target)
    if (len(target)) == 0:
        print("目标不存在\n")
        continue
    if (len(target)) == 1:
        target = target[0]
    else:
        print("命中" + str(len(target)) + "人，请选择：", end = "")
        for i in range(len(target)):
            print(target[i][1] + "(" + str(i + 1) + ")", end = "")
            if i != len(target) - 1:
                print("，", end = "")
        num = input(" ")
        while not num.isnumeric() or int(num) < 1 or int(num) > len(target):
            num = input("请重新输入合法值：")
        target = target[int(num) - 1]

    reviewee = check('e', target[0], homeworkid)
    reviewer = check('r', target[0], homeworkid)
    for review in reviewee:
        s = review["reviewer"]["fullname"] + "@" + target[1]
        s += "(" + str(review["score"]) + "): "
        s += review["comment"]
        print(s)
    print()
    for review in reviewer:
        s = target[1] + "@" + review["reviewee"]["fullname"]
        s += "(" + str(review["score"]) + "): "
        s += review["comment"]
        print(s)
    print("\n")









