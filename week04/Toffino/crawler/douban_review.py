import requests
import logging
from time import sleep
from queue import Queue
import pymysql
from lxml import etree
from pathlib import Path
import re

DEBUG = False

def parse_page(page_content):
    # 利用xpath获得评论内容
    results = []
    html = etree.HTML(page_content)
    # 获得所有评论块
    comments = html.xpath("//div[@class='comment']")
    # 遍历评论块， 取出详细内容
    for comment in comments:
        try:
            author = comment.xpath(".//span[@class='comment-info']/a/text()")[0]
            created_on = comment.xpath(".//span[@class='comment-time ']/text()")[0].strip()
            content = comment.xpath(".//span[@class='short']/text()")[0]
            rate_str = comment.xpath(".//span[@class='comment-info']/span[2]/@class")[0]
            rate_re = 'allstar(.+)0'
            rate = re.findall(rate_re, rate_str)
            rate = rate[0] if len(rate) else 0
            result = [author, content, created_on, rate]
            results.append(result)
#            logging.debug(f'result: {result}')
        except Exception as e:
            logging.error(f'抽取时有错误发生：{e}')
    
    next_url = html.xpath("//div[@id='paginator']/a[@class='next']/@href")
    next_url = next_url[0] if len(next_url) else None
    logging.info(f'next_url: {next_url}')

    # 调试时只抓取第一页，所以要把下一页的url置为空
    if DEBUG:
        next_url = None
    
    return results, next_url

def insert_db(results, db_conn):
    # 将评论插入数据库
    try:
        with db_conn.cursor() as cursor:
            sql = '''INSERT INTO review (author, content, created_on, rate) VALUES (%s, %s, %s, %s)'''
            values = tuple(results)
            cursor.executemany(sql, values)
            logging.info(f'插入了{len(results)}条评论')
        db_conn.commit()
    except Exception as e:
        logging.error(f'Database insert error: {e}')


if __name__ == '__main__':
    # 设置logging
    logging.basicConfig(level=logging.DEBUG,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(levelname)-8s %(message)s')
    
    # url的前缀和开始的url
    url_prefix = 'https://movie.douban.com/subject/34930862/comments'
    next_url = '?status=P'
    
    # 设置user-agent
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }
    
    # 创建数据库连接
    db_conn = pymysql.connect("ec2-3-137-159-11.us-east-2.compute.amazonaws.com", "django", "DjAnGo166$", "toffino")

    # 页数
    page_no = 0
    while next_url:
        page_no += 1
        # 生成页面保存文件名
        file = Path(__file__).parent.joinpath('{}.html'.format(page_no))
        if file.exists():
            # 如果文件存在则直接读取
            with open(file, 'r', encoding='utf-8') as f:
                page = f.read()
        else:
            # 如果不存在，则进行抓取，并将内容存入文件
            url = url_prefix + next_url
            logging.info(f'开始抓取: {url}')
            logging.info('等待10秒')
            sleep(10)
            page = requests.get(url, headers=headers).text
            logging.info(f'抓取结束: {url}')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(page)
        
        # 进行分析，返回结果列表和下一页的url
        results, next_url = parse_page(page)
        logging.info(f'下一页url: {next_url}')
        # 插入数据库
        if not DEBUG:
            insert_db(results, db_conn)
        
    logging.info('爬取结束')




