# coding=utf-8

import requests
import sys
import queue
import threading
from bs4 import BeautifulSoup as bs
import re

headers = {
}


class baiduSpider(threading.Thread):
    def __init__(self, queue, name):
        threading.Thread.__init__(self)
        self._queue = queue
        self._name = name

    def run(self):
        while not self._queue.empty():
            url = self._queue.get()
            self.get_url(url)


    def get_url(self, url):
        r = requests.get(url=url, headers=headers)
        soup = bs(r.content, "html.parser")
        urls = soup.find_all(name='a', attrs={'href': re.compile(('.'))})
        #        for i in urls:
        #            print i

        # 抓取百度搜索结果中的a标签，其中href是包含了百度的跳转地址

        for i in urls:
            if 'www.baidu.com/link?url=' in i['href']:
                a = requests.get(url=i['href'], headers=headers)

                # 对跳转地址进行一次访问，返回访问的url就能得到我们需要抓取的url结果了

                # if a.status_code == 200:
                # print a.url

                with open('E:/url/' + self._name + '.txt') as f:
                    if a.url not in f.read():
                        f = open('E:/url/' + self._name + '.txt', 'a')
                        f.write(a.url + '\n')
                        f.close()


def main(keyword):
    name = keyword

    f = open('E:/url/' + name + '.txt', 'w')
    f.close()

    queue = Queue.Queue()
    for i in range(0, 760, 10):
        queue.put('http://www.baidu.com/s?wd=%s&pn=%s' % (keyword, str(i)))

    threads = []
    thread_count = 10

    for i in range(thread_count):
        spider = baiduSpider(queue, name)
        threads.append(spider)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    print
    "It's down,sir!"


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print
        'no keyword'
        print
        'Please enter keyword '

        sys.exit(-1)
    else:
        main(sys.argv[1])