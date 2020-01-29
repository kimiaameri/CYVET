import requests 
from bs4 import BeautifulSoup 
import csv 
csv_file = open('wsc_scrape.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor', 'product', 'link'])



for i in range(14):
    url = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    table_main = soup.find('div', attrs = {'class':'view-content'}) 
    table_items =table_main.findAll('div', attrs = {'class':'item-list'})
    for row1 in table_items:
      vendor = row1.h3.text
      print(vendor)
      table_field=table_main.findAll('span', attrs={'class':'views-field views-field-title'})
      for row2 in table_field:
        product=row2.text
        print(product)
        link = row2.a['href']
        print(link)
        csv_writer.writerow(['vendor', 'product', 'link']
csv_file.close()

for i in range(14):
    url = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    table_main = soup.find('div', attrs = {'class':'view-content'}) 
    table_items =table_main.findAll('div', attrs = {'class':'item-list'})
    for row1 in table_items:
      vendor = row1.h3.text
      print(vendor)
      csv_writer.writerow([vendor, 'product', 'link'])
