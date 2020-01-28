#Python program to scrape CVE website and save quotes from website 

import wget
import requests 
from bs4 import BeautifulSoup 
import csv 
import html5lib

url = 'https://cve.mitre.org/data/downloads/allitems.html'

# define keywords for search OT in CVE
keyword = ['PLM Systems', 'MES applications', 'Safety Automation Systems', 
           'Building Management Systems', 'valves', 'transmitters', 'switches', 'actuators',
          'PLC','SCADA', 'DCS','CNC','RTU','SMART','embedded','Stuxnet']
r = requests.get(url) 

soup = BeautifulSoup(r.content, 'html.parser') 
print(soup.prettify()) 
cveData=[]  # a list to store all required data 
  
#table = soup.find('div', attrs = {'id':'CenterPane'}) 
  
for row in soup.findAll('div', attrs = {'id':'CenterPane'}): 
    cveData = {} 
    cveData['CVEId'] = row.h2.text 
    cveData['url'] = row.a['href'] 
    cveData['img'] = row.img['src'] 
    cveData['lines'] = row.h6.text 
    cveData['author'] = row.p.text 
    cveData.append(cveData) 
id="CenterPane"
