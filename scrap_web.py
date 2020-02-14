import nltk
nltk.download('punkt')
import nltk.corpus
import requests 
from bs4 import BeautifulSoup 
import csv 
from googlesearch import search
import urllib.request
import re
from urllib.parse import urlparse

links_google = open('linkAll.txt', 'r', encoding='utf-8')
Lines = links_google.readlines() 
for line in Lines:
    parsed_uri = urlparse(line)
    url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    #r = requests.get(url) 
    #soup = BeautifulSoup(r.content, 'html.parser') 
    vendor=re.sub(".com|.org|.edu|.net|.gov|.us/|.htm|.html|.pdf|.php|.aspx |http://| https://","",str(url))        
    text=re.sub("http://www.","",str(vendor))
    text=re.sub("https://www.","",str(text))
    vendor=re.sub("[^a-zA-Z]","",str(text))
    print(vendor)
    try:
        r = requests.get(url,verify = False)
        with open(str(vendor)+".txt", 'wb') as outfile:
             outfile.write(r.content)
    except requests.exceptions.RequestException as e:
         print(e)
         pass
