#!/usr/bin/env Python
# coding=utf-8
import time
import urllib.request
import re


def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
    response = urllib.request.urlopen(req)
    html = response.read().decode('gbk')  # gbk格式的
    return html


def search_novel():  # 实现查找到小说，并且返回该小说所在笔趣阁网页的代码
    content = input('请输入你想要查找的小说名：')
    initial_content = content
    content += ' site:guibuyu.org'
    content_code = urllib.request.quote(content)  # 解决中文编码的问题

    url = 'https://www.baidu.com/s?wd=' + content_code

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
    response = urllib.request.urlopen(req)

    html = response.read().decode('utf-8')

    link_list = re.findall(r'<div class.*?c-container[\s\S]*?href[\s\S]*?http://([\s\S]*?)"', html)

    for url in link_list:
        url = 'http://' + url

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0')
        response = urllib.request.urlopen(req)

        real_url = response.geturl()
        print('小说《' + initial_content + '》笔趣阁在线阅读地址是：' + real_url)
        return real_url


def get_title(html):
    '获取该URL页面小说的章节标题'
    p = r'<h1>(.*?)</h1>'
    title = re.findall(p, html)  # 加上()直接返回括号内的内容
    print(title[0])
    return title[0]


def get_content(html):
    '获取该URL页面的小说内容'
    p = r'<div id="content">([\s\S]*?)</div>'  # ？启用非贪婪模式
    content = re.findall(p, html)

    content[0] = content[0].replace(' ', ' ')
    content[0] = content[0].replace('<br />', '')
    content = re.sub(r'<a.*?>(.*?)</a>', '', content[0])  # 去除里面的<a>元素
    return content


def write_into_file(title, content):
    '将标题和内容写入文件'
    f = open('C:\\Users\\sky\\Desktop\\fiction.txt', 'a')
    f.writelines(title + '\n\n')
    f.writelines(content + '\n\n')
    f.close()


def get_every_page_url(content):
    '得到每页的URL'
    cut_down = re.findall(r'<div class="info_chapters">[\s\S]*?<div id="list">([\s\S]*?)</div>',
                          content)  # 初步分割网页源代码，获取我们想要的url所在的块
    spilt = re.findall(r'<dt>[\s\S]*?</dt>', cut_down[0])  # 找到“最新章节”以及“正文”
    start = cut_down[0].find(spilt[1])  # 获取“正文”标签所在的位置
    real_urls = cut_down[0][start:]  # 得到包含我们真正想要url的块
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", real_urls)  # 获取该块中所有的超链接
    return link_list


if __name__ == '__main__':
    url = search_novel()
    content = open_url(url)

    link_list = get_every_page_url(content)

    for url in link_list:
        url = 'http://www.guibuyu.org' + url
        html = open_url(url)
        time.sleep(5)  # 为了防止网站反爬，就sleep了一下。
        write_into_file(get_title(html), get_content(html))
