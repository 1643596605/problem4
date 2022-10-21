import requests
import csv
import re
import time


burl = 'https://www.zhihu.com/api/v4/creators/rank/hot?domain='
headers = {

  'Cookie': '_xsrf=o1h9dMvqHbQ40BcVdj96oLZaV4tzBdUO; KLBRSID=d6f775bb0765885473b0cba3a5fa9c12|1665675792|1665675006',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'

}
# domain=？ ？=0为全部   ？=10001为数码  ？=10002为科技  依此类推
list = ['0', '10001']
list1 = ['&period=hour',
         '&limit=20&offset=20&period=hour',
         '&limit=20&offset=40&period=hour',
         '&limit=20&offset=60&period=hour',
         '&limit=20&offset=80&period=hour']
list2 = ['链接', '题目', '关注增量', '浏览增量', '回答增量', '赞同增量', '热度值', '分类']

for iuu in list:
    f = open("知乎热搜"+iuu+".csv", mode="w", newline="", encoding='gb18030')

    csvwriter = csv.writer(f)
    csvwriter.writerow(list2)
    for iu in list1:
        url = burl+iuu+iu
        resp = requests.request("GET", url=url, headers=headers)
        page_content = resp.text
        print(resp.text)
        obj = re.compile(r'\"url\":\"(?P<lj>.*?)\",\"created.*?title\":\"(?P<tm>.*?)\",\"highl.*?new_pv\":(?P<ll>.*?),'
                        r'.*?\"new_follow_num":(?P<gz>.*?),.*?,\"new_answer_num\":(?P<hd>.*?),.*?new_upvote_num\":(?P<zt>.*?),'
                        r'.*?\"score\":(?P<sc>.*?),\"')
        result = obj.finditer(page_content)
        for it in result:
            # 进一步爬取网站信息
            iz = it.group("lj")
            print(it.group("lj"))
            resp1 = requests.request("GET", url=iz, headers=headers)
            in_content = resp1.text
            obj2 = re.compile('name=\"keywords\" content=\"(?P<fl>.*?)\"/>', re.S)
            result0 = obj2.finditer(in_content)
            time.sleep(0.5)
            for i in result0:
                print(i.group("fl"))
                dic2 = i.groupdict()
            print(it.group("tm"))
            print(it.group("sc"))
            print(it.group("ll"))
            print(it.group("gz"))
            print(it.group("hd"))
            print(it.group("zt"))
            dic1 = it.groupdict()

            dictMerged2 = dict(dic1, **dic2)

            csvwriter.writerow(dictMerged2.values())
        time.sleep(5)
    time.sleep(15)
    f.close()

print("已完成！！！")
