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
      need = {}
      for li_tag in soup.find_all('ul'):
        for span_tag in li_tag.find_all('li', {'class':'views-field views-field-title'}):
           field = span_tag.find('span', {'class':'field-content'}).text
           print(field)
           link = span_tag.find('span', {'class':'field-content'}).a
           print(link)
           csv_writer.writerow([vendor, product, link])

print(need)
      table_field=table_items.findAll('span', attrs={'class':'views-field views-field-title'})
      for row2 in table_field:
        if vendor in 
        product=row2.text
        print(product)
        link = row2.a['href']
        print(link)
        csv_writer.writerow([vendor, product, link])
csv_file.close()

for i in range(14):
    url = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'lxml') 
    table_main = soup.find('div', attrs = {'class':'view-content'}) 
    table_items =table_main.findAll('div', attrs = {'class':'item-list'})
    for row1 in table_items:
      vendor = row1.h3.text
      print(vendor)
      table_field=table_items.findAll('span', attrs={'class':'views-field views-field-title'})
      for row2 in table_field:
        if vendor in 
        product=row2.text
        print(product)
        link = row2.a['href']
        print(link)
        csv_writer.writerow([vendor, product, link])
