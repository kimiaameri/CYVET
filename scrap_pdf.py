#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 01:41:32 2020
this script will find all pdfs in all pages of each website 
@author: kimiaameri
"""
import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
from googlesearch import search
import os
main_folder=r'C:/Users/developer/Desktop/CYVET/webscraping/'
if not os.path.exists(main_folder):os.mkdir(main_folder)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
processed_vendor= set()
with open(r'C:/Users/developer/Desktop/CYVET/vendors_webcontent_Sorted_Final.csv') as f:
    reader = csv.reader(f)
    vendor_list = [r for r in reader]
    vendor_list.pop(0) # remove header
for l in range(len(vendor_list)):
    if float(vendor_list[l][3]) >50:
        vendor=vendor_list[l][0]
        processed_vendor.add(vendor)
        home_page_url=vendor_list[l][1]
# a queue of urls to be crawled next
        new_urls = deque([home_page_url])
# a set of urls that we have already processed 
        processed_urls = set()
# a set of domains inside the target website
        local_urls = set()
# a set of domains outside the target website
        foreign_urls = set()
# a set of broken urls
        broken_urls = set()
# process urls one by one until we exhaust the queue
        while len(new_urls):    # move url from the queue to processed url set   
            url = new_urls.popleft()    
            processed_urls.add(url)    # print the current url    
            print('Processing %s' % url)
            try:    
                response_link = requests.get(url,headers=headers,timeout=25)
            except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):   
# add broken urls to it’s own set, then continue    
                broken_urls.add(url)
                continue
# extract base url to resolve relative links
        parts= urlsplit(url)
        base = '{0.netloc}'.format(parts)
        strip_base = base.replace('www.', '')
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        if '/' in parts.path:
            path = url[:url.rfind('/')+1] 
        else:
            url
        
        soup = BeautifulSoup(response_link.text, "lxml")
        for link in soup.find_all('a'):    # extract link url from the anchor   
            anchor = link.attrs['href'] if "href" in link.attrs else ''
            if anchor.startswith('/'):        
                local_link = base_url + anchor        
                local_urls.add(local_link)    
            elif strip_base in anchor:        
                local_urls.add(anchor)    
            elif not anchor.startswith('http'):        
                local_link = path + anchor        
                local_urls.add(local_link)    
            else:        
                foreign_urls.add(anchor)
        if not link in new_urls and not link in processed_urls:    
            new_urls.append(link)
#--------------------------------------------------------------------------------------------
#    find pdfs
#--------------------------------------------------------------------------------------------
        folder_location = r'C:\\Users\\developer\\Desktop\\CYVET\\webscraping\\' + vendor
        if not os.path.exists(folder_location):os.makedirs(folder_location)
        for i in local_urls:
            try:
                response_i = requests.get(i, headers=headers,timeout=25,allow_redirects=True,stream=True)
                try:
                    soup_i= BeautifulSoup(response_i.text, "html.parser")     
                    for link in soup_i.select("a[href$='.pdf']"):
    #Name the pdf files using the last portion of each link which are unique in this case
                        filename = os.path.join(folder_location,link['href'].split('/')[-1])
                        with open(filename, 'wb') as f:
                            f.write(requests.get(urljoin(url,link['href']),headers=headers,timeout=25,allow_redirects=True,stream=True).content)
#--------------------------------------------------------------------------------------------
#    find products list
#--------------------------------------------------------------------------------------------
                    products=[]
                    for a in soup_i.find_all('a',href=True):
                            try:
                                products.append(a.find('h3').text)
                            except:
                                pass
                    df=pd.DataFrame({'Vendor': vendor,'Homepage':home_page_url,'Product Name':products,'Product link':i})
                    #df.to_csv(vendor+' products.csv',index=False,encoding='utf-8')
                    df.to_excel(writer,vendor)

                except Exception:
                    pass
            except Exception:
                pass
    print(l)
writer.save()
f.close()
