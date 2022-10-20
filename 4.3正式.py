
import csv
import time
import requests
import re
import pandas as pd
import os
from datetime import datetime
from threading import Timer

burl = 'https://www.bkjx.sdu.edu.cn/sanji_list.jsp?urltype=tree.TreeTempUrl'

list1 = ['&wbtreeid=1013', '&wbtreeid=1014', '&wbtreeid=1015', '&wbtreeid=1016', '&wbtreeid=1017', '&wbtreeid=1018', '&wbtreeid=1019', '&wbtreeid=1020', '&wbtreeid=1021', '&wbtreeid=1022', '&wbtreeid=1023', '&wbtreeid=1266', '&wbtreeid=1024']
list2 = ['链接', '题目', '日期']
file = "./SDU"



def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")




def task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for iu in list1:
        url = burl+iu
        resp = requests.request("GET", url=url)
        page_content = resp.text
        obj = re.compile("t\"><a href=\"(?P<qherf>.*?)\".*?title=\"(?P<title>.*?)\" style.*?right;\">\[(?P<dtime>.*?)]", re.S)
        result = obj.finditer(page_content)

        csvwriter.writerow(list2)
        for it in result:
#            print(it.group("qherf"))
#            print(it.group("title"))
#            print(it.group("dtime"))
            dic = it.groupdict()
            csvwriter.writerow(dic.values())
        time.sleep(2.5)
while True:
    mkdir(file)
    ti = datetime.now().strftime("%m %d %H %M %S")
    tti = "./SDU/"
    f = open(tti+str(ti)+'.csv', mode="w", newline="", encoding='gb18030')
    csvwriter = csv.writer(f)
    task()
    f.close()
    print("over!")
    newdir = './SDU'  # 列出文件夹下所有的目录与文件
    writer = pd.ExcelWriter('SDU.xlsx')
    list = os.listdir(newdir)
    print(list)
    for i in range(0, len(list)):
        data = pd.read_csv(tti+list[i], encoding="gb18030", index_col=0)
        data.to_excel(writer, sheet_name=list[i])
    writer.close()
    print("over！")
    time.sleep(60)







