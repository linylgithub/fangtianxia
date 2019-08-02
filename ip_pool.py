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

    def __init__(self):
        self.url_list = set()
        self.session = Session()

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

    def get_ip_list(self, page, url):
        """
        解析页面
        :param: 
        :return: 
        """  
        soup = BeautifulSoup(page, 'lxml') 
        trs = soup.find('table', id="ip_list").find_all('tr')
        ip_list = []
        for tr in trs[1:]:
            tds = tr.find_all('td')
            # print([item for item in tr.contents])
            ip = tds[1].text
            port = tds[2].text
            procotol = tds[5].text or 'http'
            proxy = (ip, port, procotol)
            if self.check_ip_use(proxy):
                ip_list.append(proxy)
        return ip_list

    def save_ip(self, ip_list, url):
        """
        解析页面
        :param: 
        :return: 
        """ 
        ip_proxy = IPProxy(ip=proxy[0], port=proxy[1], procotol=[2], source=url)
        self.session.add(ip_proxy)


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
        


if __name__ == "__main__":
    base_url = "https://www.xicidaili.com/nn/2"
    proxy = ("120.83.109.180", "9999", "http")
    ip_proxy = IPProxySpider()
    # page = ip_proxy.get_page(base_url)
    page = ip_proxy.get_page(base_url, proxy)
    if page:
        ip_list = ip_proxy.get_ip_list(page)
    # print(page.code)
        print(len(ip_list))