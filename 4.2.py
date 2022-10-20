import requests
import csv
import re
import time
# 436882694
name1 = input('输入一号待测试人员UID: ')
print('一号已完成输入！')
# 11352614
name2 = input('输入一号待测试人员UID: ')
print('二号已完成输入！')
print('请静待结果！')

burl5 = 'https://api.bilibili.com/x/relation/followings?vmid='+name1
burl6 = 'https://api.bilibili.com/x/relation/followings?vmid='+name2
headers = {
    'referer': 'https://space.bilibili.com/11352614/fans/follow',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42'
}
list1 = ['&pn=1&ps=20&order=desc&jsonp=jsonp&callback=__jp3', '&pn=2&ps=20&order=desc&jsonp=jsonp&callback=__jp11', '&pn=3&ps=20&order=desc&jsonp=jsonp&callback=__jp14', '&pn=4&ps=20&order=desc&jsonp=jsonp&callback=__jp15', '&pn=5&ps=20&order=desc&jsonp=jsonp&callback=__jp16']
list2 = []
list3 = []
list5 = ['UID', '昵称', '等级', '粉丝数']
listUID1 = []
listUID2 = []
listzong = []

# 第一人
for iu in list1:
    url = burl5+iu
    resp = requests.request("GET", url=url, headers=headers)
    page_content = resp.text
    print(page_content)
    obj = re.compile("{\"mid\":(?P<UID>.*?),", re.S)
    result = obj.finditer(page_content)

    for it in result:

        dic = it.groupdict()
        list2 = list(dic.values())
        listUID1 = list2 + listUID1
    time.sleep(2.5)

# 第二人
for iu in list1:
    url = burl6+iu
    resp = requests.request("GET", url=url, headers=headers)
    page_content = resp.text
    print(page_content)
    obj = re.compile("{\"mid\":(?P<UID>.*?),", re.S)
    result = obj.finditer(page_content)

    for it in result:

        dic = it.groupdict()
        list3 = list(dic.values())
        listUID2 = list3 + listUID2

    time.sleep(2.5)


listzong = [x for x in listUID1 if x in listUID2]
print(listzong)


# 开始生成相同数据
g = open("相同up.csv", mode="w", newline="", encoding='gb18030')
csvwriter = csv.writer(g)
csvwriter.writerow(list5)
for uid in listzong:

    url5 = 'https://api.bilibili.com/x/space/acc/info?mid='+uid+'&token=&platform=web&jsonp=jsonp'
    url6 = 'https://api.bilibili.com/x/relation/stat?vmid='+uid+'&jsonp=jsonp'
    resp5 = requests.request("GET", url=url5, headers=headers)
    resp6 = requests.request("GET", url=url6, headers=headers)
    shuju_content = resp5.text
    fensi_content = resp6.text
#    print(shuju_content)
#    print(fensi_content)
    obj5 = re.compile("\"mid\":(?P<UID>.*?),.*?name\":\"(?P<nicheng>.*?)\",\"sex.*?level\":(?P<dj>.*?),\"jointime", re.S)
    obj6 = re.compile("follower\":(?P<fensi>.*?)}}")
    result5 = obj5.finditer(shuju_content)
    result6 = obj6.finditer(fensi_content)
    for it5 in result5:
        print(it5.group("UID"))
        print(it5.group("nicheng"))
        print(it5.group("dj"))
        dic5 = it5.groupdict()
        for it6 in result6:
            print(it6.group("fensi"))
            dic6 = it6.groupdict()
        dictMerged5 = dict(dic5, **dic6)
        csvwriter.writerow(dictMerged5.values())
g.close()
print('匹配完成！')
