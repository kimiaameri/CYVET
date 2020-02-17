import nltk
nltk.download('punkt')
import nltk.corpus
import requests 
from bs4 import BeautifulSoup 
import csv 
from googlesearch import search
import re
from urllib.parse import urlparse
from flashtext.keyword import KeywordProcessor
#----------------------------------------------------------------------------
#                                   find score                            
#----------------------------------------------------------------------------

keywords_menu = ['IOT', 'bussiness','product', 'solution', 'tools', 'contact','industial','support']
keyword_maintext= ['Control Systems', 'Electronics','Embedded','Industial','manufacture','industrial IOT','certificate']
keywords=keywords_menu + keyword_maintext
kp0=KeywordProcessor()

for word in keywords:
    kp0.add_keyword(word)
kp1=KeywordProcessor()
for word in keywords_menu:
    kp1.add_keyword(word)
kp2=KeywordProcessor()
for word in keyword_maintext:
    kp2.add_keyword(word)

def percentage(dum0,dumx):
    try:
        ans=float(dumx)/float(dum0)
        ans=ans*100
    except:
        return 0
    else:
        return ans 

def find_score(text):
    #Lines = text.readlines()
    x=str(text)
    y0 = len(kp0.extract_keywords(x))
    y1 = len(kp1.extract_keywords(x))
    y2 = len(kp2.extract_keywords(x))
    #Total_matches=y0   
    per1 = float(percentage(y0,y1))
    per2 = float(percentage(y0,y2))
    if y0==0:
        score=0
    else:
        if per1>=per2 :
            score=per1
        elif per2>=per1:
            score=per2
    return score

#----------------------------------------------------------------------------
#                                   find vendors and scrap webcontent                            
#----------------------------------------------------------------------------

csv_file = open('vendors_webcontent.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor','url','link','score','userfeedback'])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
for i in range(14):
    URL = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(URL, headers=headers) 
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
                  search_page = requests.get(link, headers=headers)        #to extract page from website
                  html_search_page = search_page.content
                  try:
                          soup1 = BeautifulSoup(html_search_page, 'html.parser')  #Parse html code
                          with open(str(name)+".txt", 'wb') as outfile:
                              text=soup1.encode('utf-8').strip()
                              text_main = soup1.find('body')
                              score1=find_score(text_main)
                              outfile.write(soup1.encode('utf-8').strip())
                  except requests.exceptions.RequestException:
                      pass
              except Exception:
                  pass             
              try:    
                  home_url = urlparse(link)
                  url = '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
                  home_page = requests.get(url, headers=headers)        #to extract page from website
                  html_home_page = home_page.content        #to extract html code from page
                  try:
                      soup1 = BeautifulSoup(html_home_page, 'html.parser')  #Parse html code
                      text=soup1.encode('utf-8').strip()
                      text_main = soup1.find('body')
                      score2=find_score(text_main)
                  except requests.exceptions.RequestException:
                      pass
              except Exception:
                  pass
              if score1>score1:
                  score=score1
              else:
                  score=score2
              csv_writer.writerow([vendor,url, link,score])
      else:
          vendor=group_vendors
          print(vendor)
          name=re.sub("[^a-zA-Z]","",str(vendor))
          for k in search(vendor, num=3,stop=1, pause=2):
              link=k
              try:
                  search_page = requests.get(link, headers=headers)        #to extract page from website
                  html_search_page = search_page.content
                  try:
                          soup1 = BeautifulSoup(html_search_page, 'html.parser')  #Parse html code
                          with open(str(name)+".txt", 'wb') as outfile:
                              text=soup1.encode('utf-8').strip()
                              text_main = soup1.find('body')
                              score1=find_score(text_main)
                              outfile.write(soup1.encode('utf-8').strip())
                  except requests.exceptions.RequestException:
                      pass
              except Exception:
                  pass             
              try:    
                  home_url = urlparse(link)
                  url = '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
                  home_page = requests.get(url, headers=headers)        #to extract page from website
                  html_home_page = home_page.content        #to extract html code from page
                  try:
                      soup1 = BeautifulSoup(html_home_page, 'html.parser')  #Parse html code
                      text=soup1.encode('utf-8').strip()
                      text_main = soup1.find('body')
                      score2=find_score(text_main)
                  except requests.exceptions.RequestException:
                      pass
              except Exception :
                  pass
              if score1>score1:
                  score=score1
              else:
                  score=score2
              csv_writer.writerow([vendor, url,link,score])
          #urllib.request.urlretrieve(link,str(vendor)+".txt")
csv_file.close()
#----------------------------------------------------------------------------
#                                   remove duplicates                            
#----------------------------------------------------------------------------
lines_seen = set() # holds lines already seen
outfile = open('vendors_webcontent.csv', "w")
for line in open('vendors_webcontent.csv', "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()


