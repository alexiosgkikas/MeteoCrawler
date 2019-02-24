# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 14:20:07 2019

@author: Alexios

The code for Proxy was taken by https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]


class Proxies:
    urlproxy = 'https://www.sslproxies.org/'
    proxies = []
    good_proxies = []
    start_time = time.time()
    
    # Construct Set url with proxies list and how many working proxies to retrieve
    def __init__(self, urlproxy='https://www.sslproxies.org/', number_of_proxies=1):
        self.urlproxy=urlproxy
        self.num_prox = number_of_proxies
    """
        Function, which retrieve number of working proxies from site 
    """
    def getProxiesAllInOne(self):
        ua = UserAgent() # From here we generate a random user agent
        proxies_req = Request(self.urlproxy)
        proxies_req.add_header('User-Agent', ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                    'ip':   row.find_all('td')[0].string,
                    'port': row.find_all('td')[1].string
                    })
        
        good_proxies = []
        while len(good_proxies) < self.num_prox:
            print('Try finding proxy # '+str(len(good_proxies)))
            proxy_index = random.randint(0,(len(proxies)-1))
            proxy = proxies[proxy_index]
            # Try making the call and if it was successfull save it in list  
            try:
                req = Request('http://icanhazip.com')
                req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
                urlopen(req,timeout = 2).read().decode('utf8')
                print('Working Proxy ' +proxy['ip'] + ':' + proxy['port'])
                good_proxies.append(proxy)
            except: # If occurs error delete the proxy
              del proxies[proxy_index]
              print('Not Working Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
        
        return good_proxies
    """
        Get list of proxies online
    """
    def getProxiesListFromOnline(self):
        ua = UserAgent() # From here we generate a random user agent
        proxies_req = Request(self.urlproxy)
        proxies_req.add_header('User-Agent', ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')
        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({'ip':row.find_all('td')[0].string,'port': row.find_all('td')[1].string})
        return proxies
    
    """
        Get list of good proxies 
    """
    def getProxy(self,num_proxies_to_get, sec_until_renew_list):
        good_proxies = [] # list where good proxies are store
        while len(good_proxies) < num_proxies_to_get:
            elapsed_time = time.time() - self.start_time
            if len(self.proxies) == 0  or  elapsed_time >= sec_until_renew_list:
                 print('There is no other proxy in list or time passed sinced requested list,so would make request for new list of proxies')
                 self.proxies = self.getProxiesListFromOnline()
                 self.start_time = time.time()
            print('Size of Proxy List: '+str(len(self.proxies)))     
            print('Try finding proxy # '+str(len(good_proxies)))
            proxy_index = random.randint(0,(len(self.proxies)))
            proxy = self.proxies[proxy_index]
            # Try making the call and if it was successfull save it in list  
            try:
                req = Request('http://icanhazip.com')
                req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
                urlopen(req,timeout = 2).read().decode('utf8')
                print('Working Proxy ' +proxy['ip'] + ':' + proxy['port'])
                good_proxies.append(proxy)
                del self.proxies[proxy_index] # so it would never occur again
            except: # If occurs error delete the proxy
                del self.proxies[proxy_index]
                print('Not Working Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
        
        return good_proxies