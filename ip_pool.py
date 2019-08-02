#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# author: linyl
# Date: 2019-08-01 14:33:19
# Description: IP代理相关操作
"""
import logging
import requests
import random
from bs4 import BeautifulSoup
from config import USER_AGENT

from model import IPProxy, Session

class IPProxySpider(object):
    """ip代理类"""

    def __init__(self, base_url, host):
        self.new_url_list = set()
        self.old_url_list = set()
        self.new_url_list.add(base_url)
        self.session = Session()  
        self.base_url =  host     

    def run(self):
        url = self.new_url_list.pop()
        proxy = self.get_proxy
        page = self.get_page(url, proxy)
        ip_count = 0
        if page:
            self.old_url_list.add(url)
            ip_count = self.parse_page(page, url)
        return ip_count


    def get_url(self, page):
        pass

    def get_page(self, url, proxy=None):
        """
        获取yem
        :param: 
        :return: 
        """   
        try:
            header = {'User-Agent': random.choice(USER_AGENT)}
            if proxy:
                session = requests.Session()
                session.trust_env = False
                proxies = {f'{proxy[2]}': f"{proxy[2]}://{proxy[0]}:{proxy[1]}"}
                print(proxies)
                r = session.get(url, headers=header, proxies=proxies, timeout=5) 
            else:
                r = requests.get(url, headers=header, timeout=5)
            return r.text
        except Exception as e:
            logging.error(e)
            return None

    def get_proxy(self):
        """
        获取代理
        :param: 
        :return: 
        """   

    def parse_page(self, page, url):
        """
        解析页面
        :param: 
        :return: 
        """  
        soup = BeautifulSoup(page, 'lxml') 
        trs = soup.find('table', id="ip_list").find_all('tr')
        urls = soup.find('div', _class="pagaination").find_all('a')
        for _url in urls:
            new_url = self.base_url + _url.href
            self.new_url_list.add(new_url)
        ip_count = 0
        proxy_list = []
        for tr in trs[1:]:
            tds = tr.find_all('td')
            # print([item for item in tr.contents])
            ip = tds[1].text
            port = tds[2].text
            procotol = tds[5].text or 'http'
            proxy = (ip, port, procotol)
            if self.check_ip_saved(proxy):
                continue
            if self.check_ip_use(proxy):
                # self.save_ip(proxy, url)
                proxy_list.append(IPProxy(ip=proxy[0], port=proxy[1], procotol=proxy[2], source=url))
                ip_count += 1
                print(proxy)
                # ip_list.append(proxy)
        self.session.add_all(proxy_list)
        self.session.commit()
        return ip_count

    def check_ip_use(self, proxy):
        """
        检查ip是否可用
        :param: 
        :return: 
        """  
        try:
            header = {'User-Agent': random.choice(USER_AGENT)}
            session = requests.Session()
            session.trust_env = False
            proxies = {f'{proxy[2]}': f"{proxy[2]}://{proxy[0]}:{proxy[1]}"}
            req =requests.get("https://ip.cn", proxies=proxies, timeout=2, headers=header)
            if req.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"msg: {proxy}, error: {e}")
            return False
    
    def check_ip_saved(self, proxy):
        """
        检查数据库是否已存有该ip
        :param: 
        :return: 
        """
        proxy = self.session.query(IPProxy).filter(IPProxy.ip == proxy[0], IPProxy.port == proxy[1], 
                    IPProxy.procotol == proxy[2], IPProxy.status == 'normal').one_or_none()
        if proxy:
            return True
        else:
            return False
        


if __name__ == "__main__":
    base_url = "https://www.xicidaili.com/nn/1"
    host = "https://www.xicidaili.com"
    proxy = ("120.83.109.180", "9999", "http")
    spider = IPProxySpider(base_url, host)
    # page = spider.get_page(base_url)
    page = spider.get_page(base_url, proxy)
    if page:
        ip_count = spider.parse_page(page ,base_url)
        print(ip_count)