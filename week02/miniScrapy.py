import requests
from lxml import etree
from queue import Queue
import threading
import json

class CrawlThread(threading.Thread):
    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    def run(self):
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    def scheduler(self):
        while not self.queue.empty():
            page = self.queue.get()
            print(f'下载线程：{self.thread_id}, 下载页面：{page}')
            url = f'https://book.douban.com/top250?start={page*25}'

            try:
                response = requests.get(url, headers=self.headers)
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常', e)


class ParserThread(threading.Thread):
    def __init__(self, thread_id, queue, file):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.file = file
    
    def run(self):
        print(f'启动线程：{self.thread_id}')
        while flag:
            try:
                item = self.queue.get(False)
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()
            except Exception as e:
                pass
        print(f'结束线程：{self.thread_id}')
    
    def parse_data(self, item):
        try:
            html = etree.HTML(item)
            books = html.xpath('//div[@class="pl2"]')
            for book in books:
                try:
                    title = book.xpath('./a/text()')
                    link = book.xpath('./a/@href')
                    response = {
                        'title': title,
                        'link': link
                    }
                    json.dump(response, fp=self.file, ensure_ascii=False)
                except Exception as e:
                    print('book error', e)
        except Exception as e:
            print('page error', e)
            

if __name__ == '__main__':

    # 定义存放网页的任务队列
    pageQueue = Queue(20)
    for page in range(0, 11):
        pageQueue.put(page)

    # 定义存放解析数据的任务队列
    dataQueue = Queue()

    # 爬虫线程
    crawl_thread = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue)
        thread.start()
        crawl_thread.append(thread)
    
    with open('book.json', 'a', encoding='utf-8') as pipeline_f:
        parse_thread = []
        parser_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)
        
        # 结束crawl线程
        for t in crawl_thread:
            t.join()
        
        # 结束parse线程
        flag = False
        for t in parse_thread:
            t.join()

        

    print('退出主线程')