from requests import get
from re import findall
from time import sleep

def get_pages():#获取动漫资源的页数
    from_url = 'http://www.llss.news/wp/category/all/anime/'
    res_get = get(from_url)
    res = findall(r'>第 1 页，共 ([1-9]\d+) 页</span>', res_get.text)
    return int(res[0])

def download(each_url):#获取每一个资源的磁力链
    url_text = get(each_url).text
    res_magnet = findall(r'([0-9a-fA-F]{40})', url_text)#可能有多个
    res_title = findall(r'<h1 class="entry-title">(.*?)</h1>', url_text)#唯一的
    with open('./magnet_links.txt', 'a+', encoding = 'utf-8') as f:
        if res_title is not None:
            f.write(res_title[0] + ':\n')
            for each in res_magnet:
                f.write('        magnet:?xt=urn:btih:' + each + '\n')
        else:
            print('Cannot find suitable links! Skip it!')
            return

def visit_each_page(pages):#进入每一个页面找资源
    root_url = 'http://www.llss.news/wp/category/all/anime/page/'
    for i in range(1, pages + 1):
        print('Now in page %d'%i)
        now_url = root_url + str(i) + '/'
        now_page_text = get(now_url).text
        now_res = findall('href="(http://www.llss.news/wp/all/anime/.*?more.*?)"', now_page_text)
        for each in now_res:
            download(each)
            print('sleep for 0.1s')
            sleep(0.1)
if __name__ == "__main__":
    pages = get_pages()
    visit_each_page(pages)
