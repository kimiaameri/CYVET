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
          'PLC','SCADA', 'DCS','CNC','RTU','SMART','embedded','Stuxnet','iLnkP2P']
#list of tools to attack
Tools=['Oscilloscope','Logic Analyzer', 'Salae','JTAG','GoodFET', 'BusBlaster', 'BusPirate',
'JTAGulator', 'JTAGenum', 'Black Magic','Probe','ChipWhisperer','power analysis', 'glitching',
 'USB', 'Facedancer','SDR', 'HackRF','P2P']
# list of attacks to IOT devices
attacks=['UART','U-Boot','Bruteforce','Xiaomi Vacuum','UART', 'JTAG','denial-of-service','Mirai','DDoS','botnet attacks','TDoS']

#IOT companies
companies =['HiChip', 'TENVIS', 'SV3C', 'VStarcam', 'Wanscam', 'NEO Coolcam', 'Sricam', 'Eye Sight', 'HVCAM']
r = requests.get(url) 

soup = BeautifulSoup(r.content, 'html.parser') 
print(soup.prettify()) 

  
#soup = BeautifulSoup(r.content, 'html5lib') 
  
cveData=[]  # a list to store all required data 
  
#table = soup.find('div', attrs = {'id':'GeneratedTable'}) 
  
for row in soup.findAll('div', attrs = {'id':'GeneratedTable'}): 
    cveData = {} 
    cveData['CVEId'] = row.h2.text 
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
