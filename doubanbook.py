import requests
from bs4 import BeautifulSoup
import time
import lxml
import os
import string
from multiprocessing import Process, Queue, Pool

class BookSpider():
    def __init__(self):
        self.init_url = 'https://read.douban.com/columns/category/all?sort=hot&start='
        self.folder_path = 'F:\DoubanBook'
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print("创建名字叫做" + path + '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            # print(path, '文件夹已存在。')
            return False

    def download_one(self,url,name,directory):
        self.mkdir(directory)
        os.chdir(directory)
        # 如果文件已经存在，放弃下载
        if os.path.exists(name):
            print(name+'已存在！')
            return
        resp = requests.get(url)
        print('开始下载', url)
        with open(name, 'wb') as f:
            f.write(resp.content)
            print('下载完成', url)

    def spider(self):
        print('Start')
        start_time = time.time()  # 计算爬虫时间

        self.mkdir(self.folder_path)
        print('切换至主文件夹')
        os.chdir(self.folder_path)
        for i in range(0,2000,10):  #这里的  range（初始，结束，间隔）
            html = requests.get(url=('https://read.douban.com/columns/category/all?sort=hot&start=%d' % i), headers=self.headers).text
            bsObj = BeautifulSoup(html, 'lxml')
            all_li = bsObj.find('ul',{'class':"list-lined"}).find_all('li')

            for li in all_li:
                book_img = li.find('img')['src']
                book_name = li.find('h4').get_text().replace(string.punctuation,'').replace('!','').replace('/','')
                book_author = li.find('div', {'class': 'author'}).find('a').get_text().replace('| ','').replace(string.punctuation,'')
                # book_cate = li.find('div', {'class': 'category'}).get_text().replace('\"', '').replace('\n','').replace('\!','').replace('?','').replace('\/','').replace(' ','')[2:]
                book_cate = li.find('div', {'class': 'category'}).get_text().replace(string.punctuation,"").replace('\n','')[2:]
                end_index = book_img.index('?')
                book_img_url = book_img[:end_index]
                img_name = book_author + ' - ' + book_name+'.jpg'
                directory = self.folder_path+'\\'+book_cate
                self.download_one(book_img_url,img_name,directory)
            print("已经完成第%d页采集，休息1s" % (i/10 + 1))
            time.sleep(1)

        end_time = time.time()
        print("爬虫花费时间为；%d s" % (end_time-start_time))

bookSpider = BookSpider()
bookSpider.spider()

