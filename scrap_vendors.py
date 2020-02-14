import nltk
nltk.download('punkt')
import nltk.corpus
import requests 
from bs4 import BeautifulSoup 
import csv 
from googlesearch import search
import re
csv_file = open('vendors_webcontent.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor','link'])
for i in range(14):
    url = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    table_main = soup.find('div', attrs = {'class':'view-content'}) 
    table_items =table_main.findAll('div', attrs = {'class':'item-list'})
    for row1 in table_items:
      group_vendors = row1.h3.text
      if (',' in group_vendors):
          vendors= group_vendors.split(', ')
          for j in range(len(vendors)-1):
              vendor=vendors[j]
              print(vendor)
              name=re.sub("[^a-zA-Z]","",str(vendor))
              for k in search(vendor, num=3,stop=1, pause=2):
                  link=k
              try:
                  page = requests.get(link,verify = False)        #to extract page from website
                  html_code = page.content        #to extract html code from page

                  try:
                          soup1 = BeautifulSoup(html_code, 'html.parser')  #Parse html code
                          with open(str(name)+".txt", 'wb') as outfile:
                              outfile.write(soup1.encode('utf-8'))
                  except requests.exceptions.RequestException as e:
                      print(e)
                      pass
              except Exception as e:
                  print(e)
                  pass
              csv_writer.writerow([vendor, link])
      else:
          vendor=group_vendors
          print(vendor)
          name=re.sub("[^a-zA-Z]","",str(vendor))
          for k in search(vendor, num=3,stop=1, pause=2):
              link=k
              try:
                  page = requests.get(link,verify = False)        #to extract page from website
                  html_code = page.content        #to extract html code from page
                  try:
                          soup1 = BeautifulSoup(html_code, 'html.parser')  #Parse html code
                          with open(str(name)+".txt", 'wb') as outfile:
                              outfile.write(soup1.encode('utf-8'))
                  except requests.exceptions.RequestException as e:
                      print(e)
                      pass
              except Exception as e:
                  print(e)
                  pass
              csv_writer.writerow([vendor, link])
          #urllib.request.urlretrieve(link,str(vendor)+".txt")
csv_file.close()
