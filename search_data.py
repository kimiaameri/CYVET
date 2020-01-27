#Python program to scrape CVE website and save quotes from website 

import wget
import requests 
from bs4 import BeautifulSoup 
import csv 
import html5lib

url = 'https://cve.mitre.org/data/downloads/allitems.xml'
r = requests.get(url) 

soup = BeautifulSoup(r.content, 'html5lib') 
print(soup.prettify()) 

  
soup = BeautifulSoup(r.content, 'html5lib') 
  
cveData=[]  # a list to store all required data 
  
table = soup.find('div', attrs = {'id':'container'}) 
  
for row in table.findAll('div', attrs = {'class':'cveData'}): 
    cveData = {} 
    cveData['CVEId'] = row.h5.text 
    cveData['url'] = row.a['href'] 
    cveData['img'] = row.img['src'] 
    cveData['lines'] = row.h6.text 
    cveData['author'] = row.p.text 
    cveData.append(cveData) 
  
filename = 'cveData.csv'
with open(filename, 'wb') as f: 
    w = csv.DictWriter(f,['CVEId','url','img','lines','author']) 
    w.writeheader() 
    for quote in quotes: 
        w.writerow(quote) 
