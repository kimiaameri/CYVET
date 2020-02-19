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
from tldextract import extract
#----------------------------------------------------------------------------
#         function to calculate the percentage of each keyword in text                          
#----------------------------------------------------------------------------
keywords_main_page = ['IOT', 'security','product', 'advisor','solution', 'vendor','industial']
keyword_text= ['Control Systems', 'Electronics','Embedded','cybersecurity','manufacture', 'IOT','certificate']
keywords=keywords_main_page + keyword_text
kp0=KeywordProcessor()
for word in keywords:
    kp0.add_keyword(word)
kp1=KeywordProcessor()
for word in keywords_main_page:
    kp1.add_keyword(word)
kp2=KeywordProcessor()
for word in keyword_text:
    kp2.add_keyword(word)

def percentage(dum0,dumx):
    try:
        ans=float(dumx)/float(dum0)
        ans=ans*100
    except:
        return 0
    else:
        return ans 
#----------------------------------------------------------------------------
#           function to find score                            
#----------------------------------------------------------------------------
def find_score(text_from_html):
    x=str(text_from_html)
    y0 = len(kp0.extract_keywords(x))
    y1 = len(kp1.extract_keywords(x))
    y2 = len(kp2.extract_keywords(x))
    per1 = float(percentage(y0,y1))
    per2 = float(percentage(y0,y2))
    if y0==0:
        score=0
        Category='Not a vendor website'
    else:
        if per1>=per2 :
            score=per1
            Category='A possible vendor homepage'
        elif per2>=per1:
            score=per2
            Category='A possible vendor website'
    return score,Category
#----------------------------------------------------------------------------
#                                   find vendors and scrap webcontent                            
#----------------------------------------------------------------------------
csv_file = open('vendors_webcontent.csv', 'w+', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor','Homepage','link','score','Category','userfeedback'])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
vendors_list=[]
for i in range(14):
    main_URL = 'https://www.us-cert.gov/ics/advisories-by-vendor?page={}'.format(i)
    r = requests.get(main_URL, headers=headers) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    table_main = soup.find('div', attrs = {'class':'view-content'}) 
    table_items =table_main.findAll('div', attrs = {'class':'item-list'})
    for row1 in table_items:
      group_vendors = row1.h3.text
      if (',' in group_vendors):
          vendors= group_vendors.split(', ')
          for j in range(len(vendors)):
              namevendor=vendors[j]
              if namevendor not in vendors_list:
                  vendors_list.append(namevendor)
                  print(namevendor)
                  name=re.sub("[^a-zA-Z0-9]","",str(namevendor))
                  for k in search(name, num=3,stop=1, pause=2):
                      link=k
                  try:    
                      home_url = urlparse(link)
                      home_page_url= '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
                      tsd, td, tsu = extract(home_page_url)
                      vendor=td
                      home_page = requests.get(home_page_url, headers=headers)        #to extract page from website
                      html_home_page = home_page.content        #to extract html code from page
                      try:
                          soup_home_page = BeautifulSoup(html_home_page, 'html.parser')  #Parse html code
                          with open(str(vendor)+".txt", 'wb') as outfile:
                              home_page_soup=soup_home_page.encode('utf-8').strip()
                              text_home_page = soup_home_page.find('body')
                              score_home_page,Category_home_page=find_score(text_home_page)
                              outfile.write(home_page_soup)
                      except requests.exceptions.RequestException:
                           pass
                  except Exception:
                      pass              
                  try:
                      search_page = requests.get(link, headers=headers)        #to extract page from website
                      html_search_page = search_page.content
                      try:
                          soup_search_page = BeautifulSoup(html_search_page, 'html.parser')  #Parse html code
                          text=soup_search_page.encode('utf-8').strip()
                          text_search_page = soup_search_page.find('body')
                          score_search_page,Category_search=find_score(text_search_page)
                      except requests.exceptions.RequestException:
                          pass
                  except Exception:
                      pass             
                  if score_home_page>score_search_page:
                      score=score_home_page
                      Category=Category_home_page
                  else:
                      score=score_search_page
                      Category=Category_search
                  csv_writer.writerow([vendor,home_page_url, link,score,Category])
      else:
          namevendor=group_vendors
          if namevendor not in vendors_list:
                  vendors_list.append(namevendor)
                  print(namevendor)
                  name=re.sub("[^a-zA-Z0-9]","",str(namevendor))
                  for k in search(name, num=3,stop=1, pause=2):
                      link=k
                  try:    
                      home_url = urlparse(link)
                      home_page_url= '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
                      tsd, td, tsu = extract(home_page_url)
                      vendor=td
                      home_page = requests.get(home_page_url, headers=headers)        #to extract page from website
                      html_home_page = home_page.content        #to extract html code from page
                      try:
                          soup_home_page = BeautifulSoup(html_home_page, 'html.parser')  #Parse html code
                          with open(str(vendor)+".txt", 'wb') as outfile:
                              home_page_soup=soup_home_page.encode('utf-8').strip()
                              text_home_page = soup_home_page.find('body')
                              score_home_page,Category_home_page=find_score(text_home_page)
                              outfile.write(home_page_soup)
                      except requests.exceptions.RequestException:
                           pass
                  except Exception:
                      pass              
                  try:
                      search_page = requests.get(link, headers=headers)        #to extract page from website
                      html_search_page = search_page.content
                      try:
                          soup_search_page = BeautifulSoup(html_search_page, 'html.parser')  #Parse html code
                          text=soup_search_page.encode('utf-8').strip()
                          text_search_page = soup_search_page.find('body')
                          score_search_page,Category_search=find_score(text_search_page)
                      except requests.exceptions.RequestException:
                          pass
                  except Exception:
                      pass             
          if score_home_page>score_search_page:
                score=score_home_page
                Category=Category_home_page
          else:
                score=score_search_page
                Category=Category_search
          csv_writer.writerow([vendor,home_page_url, link,score,Category])
