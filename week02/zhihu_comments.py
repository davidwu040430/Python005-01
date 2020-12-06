import requests
import json
from queue import Queue
import threading
import logging
from time import sleep

class CrawlThread(threading.Thread):
    def __init__(self, thread_id, queue, flag):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        self.flag = flag

    def run(self):
        logging.info(f'启动下载线程：{self.thread_id}')
        self.scheduler()
        logging.info(f'结束下载线程：{self.thread_id}')

    def scheduler(self):
        while not self.flag['url_end']:
            while not self.queue.empty():
                url = self.queue.get()
                logging.info(f'下载线程：{self.thread_id}, 下载页面：{url}')

                try:
                    response = requests.get(url, headers=self.headers)
                    # 由于知乎api不回复encoding，所以request的自动解析会解析错，形成乱码，所以直接手动解析
                    dataQueue.put(response.content.decode('utf-8'))
                except Exception as e:
                    logging.error(f'下载出现异常：{e}')
            logging.debug(f'{self.thread_id} 队列里面没有url，sleep 3秒')
            sleep(3)
    
class ParseThread(threading.Thread):
    def __init__(self, thread_id, queue, file, flag):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.file = file
        self.flag = flag
    
    def run(self):
        logging.info(f'启动解析线程：{self.thread_id}')
        while not self.flag['crawl_end']:
            try:
                while not self.queue.empty():
                    page = self.queue.get()
                    self.parse_data(page)
                    self.queue.task_done()
            except Exception as e:
                logging.error(f'{self.thread_id} 出现错误：{e}')
            logging.info(f'{self.thread_id} 结果队列里面没有结果，等待3秒')
            sleep(3)
        logging.info(f'解析线程结束：{self.thread_id}')
    
    def parse_data(self, page):
        try:
            result = json.loads(page)
            # 如果不是最后一页，则把next page的url放进抓取队列里
            if not result['paging']['is_end']:
                pageQueue.put(result['paging']['next'])
                logging.info(f"{thread_id} 增加到抓取队列：{result['paging']['next']}")
            else:
                logging.info(f'{thread_id} 遇到最后一页，置flag')
                self.flag['url_end'] = True
            
            # 解析comments
            for data in result['data']:
                content = data['content']
                author = data['author']['member']['name']
                comment = {
                    'content': content,
                    'author': author
                }
                logging.info(f"{comment['author']}:{comment['content']}")
                json.dump(comment, fp=self.file, ensure_ascii=False)
        except Exception as e:
            logging.error(f'解析遇到错误：{e}')


if __name__ == '__main__':
    # 标志位，一个是判断是否会有新增url，一个判断爬虫线程是否已经结束
    flag = {'url_end': False,
            'crawl_end': False
    }
    # 配置logging
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(levelname)-8s %(message)s')

    # 两个队列，一个是url队列，一个是结果队列
    pageQueue = Queue(20)
    pageQueue.put('https://www.zhihu.com/api/v4/zvideos/1302663458526101504/root_comments?order=normal&limit=20&offset=0&status=open')

    dataQueue = Queue()

    # 爬虫线程
    crawl_thread = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue, flag)
        thread.start()
        crawl_thread.append(thread)

    with open('comments.json', 'a', encoding='utf-8') as pipeline_f:
        parse_thread = []
        parse_name_list = ['parse_1', 'parse_2', 'parse_3']
        flag['crawl_end'] = False
        for thread_id in parse_name_list:
            thread = ParseThread(thread_id, dataQueue, pipeline_f, flag)
            thread.start()
            parse_thread.append(thread)
        
        # 等待线程结束
        for t in crawl_thread:
            t.join()
        
        flag['crawl_end'] = True
        for t in parse_thread:
            t.join()

    logging.info('退出主线程')