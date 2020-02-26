#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 16:49:17 2020

@author: kimiaameri
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 04:03:05 2020

@author: kimiaameri
"""
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
import pandas as pd
import numpy as np
from more_itertools import unique_everseen
from nltk.stem.lancaster import LancasterStemmer
import time
import json
import datetime
#----------------------------------------------------------------------------
#         function to calculate the percentage of each keyword in text   
#                       Jaccard Similarity                       
#----------------------------------------------------------------------------
keywords_main_page = ['iot system ', 'cybersecurity','vendor','industr','certificate'
                     ,'solution', 'industrial iot', 'automation','security attcak','solution',
                     'industrial authomation','industrial system','iot advisor']
keywords_menu= ['IoT ', 'industrial','automation','security', 'advisor',
                      'manufactur','inventor','vendor','control system']
keywords=keywords_main_page + keywords_menu
kp0=KeywordProcessor(case_sensitive=False)
for word in keywords:
    kp0.add_keyword(word)
kp_main=KeywordProcessor(case_sensitive=False)
for word in keywords_main_page:
    kp_main.add_keyword(word)
kp_menu=KeywordProcessor(case_sensitive=False)
for word in keywords_menu:
    kp_menu.add_keyword(word)

def percentage(dum0,dumx):
    try:
        ans=float(dumx)/float(dum0)
        ans=ans*100
    except:
        return 0
    else:
        return ans 
 
#----------------------------------------------------------------------------
#           function jacard similarity                            
#----------------------------------------------------------------------------
def get_jaccard_sim(x_main, x_menu): 
        a_main = len(set(x_main))
        a_menu = len(set(x_menu))
        b_main = len(set(keywords_main))
        b_menu=len(set(keywords_menu))
        y_main = len(set(kp_main.extract_keywords(x_main)))
        y_menu = len(set(kp_menu.extract_keywords(x_menu)))
        jacard_value_main=float(y_main / (a_main+b_main-y_main))
        jacard_value_menu=float(y_menu /( a_menu+b_menu-y_menu))
        return jacard_value_main,jacard_value_menu
#----------------------------------------------------------------------------
#           function to find score with jacard similarity                            
#----------------------------------------------------------------------------
def find_score(finaltext):
    x=str(finaltext)
    y0 = len(kp0.extract_keywords(x))
    y1 = len(kp_main.extract_keywords(x))
    y2 = len(kp_menu.extract_keywords(x))
    per1 = float(percentage(y0,y1))
    per2 = float(percentage(y0,y2))
    if y0==0:
        score=0
        Category='Not a vendor website'
    else:
        if per1>=per2 :
            score=per1
            Category='A possible vendor webpage'
        elif per2>=per1:
            score=per2
            Category='A possible vendor homepage'
    return score,Category


#----------------------------------------------------------------------------
#               scrap webcontent , return menu and main parageraph text                          
#----------------------------------------------------------------------------
def scrap_html(home_page_url,vendor):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        r=''
        finaltext=''
        r = requests.get(home_page_url, headers=headers,timeout=25)         
        html_doc = r.content 
        menu_text=[]
        main_text=[]
        html_text=''
        if r != '':
            try:
                soup = BeautifulSoup(html_doc, 'html.parser')
                texts = soup.findAll(text=True)
                text_from_html=' '.join(texts)
                html_text=re.sub("[^a-zA-Z0-9]"," ",str(text_from_html))
                for script in soup(["script", "style"]):
                    soup.text.strip().replace('\n',' ')
                with open(str(vendor)+"_html.txt", 'w') as vendor_text:
                    for p_tag_data in soup.find_all('p'):
                        main_text.append(p_tag_data.text.replace('\n | \t',' '))
                    for div_tag_data in soup.find_all('div'):
                        main_text.append(div_tag_data.text.replace('\n',' ').replace('\t',' '))
                    for li_tag_data in soup.find_all('li'):
                        menu_text.append(li_tag_data.text.replace('\n',' ').replace('\t',' '))
                    finaltext=str(main_text+ menu_text)
                    vendor_text.write(finaltext)
            except Exception:
                pass
    except Exception:
            html_text=''
            pass  
    if r =='':
        flag=False
    else:
        flag =True
    return finaltext,flag,html_text
#----------------------------------------------------------------------------
#                                   find vendors and scrap webcontent                            
#----------------------------------------------------------------------------
csv_file = open('vendors_webcontent.csv', 'w+', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor','Homepage','link','score','Category','userfeedback','html_text'])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
vendors_list=[]
for i in range(20):
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
              name=re.sub("[^a-zA-Z0-9]","",str(namevendor))
              for k in search(name+'product', num=3,stop=1, pause=2):
                  link=k
                  print(namevendor,link)
                  home_url = urlparse(link)
                  home_page_url= '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
                  tsd, td, tsu = extract(home_page_url)
                  vendor=td
                  if vendor not in vendors_list:
                      finaltext,flag,html_text = scrap_html(home_page_url,vendor)
                      if flag==True:
                          score,Category=find_score(finaltext)
                      else:
                          score=0
                          Category="not founded"
                      csv_writer.writerow([vendor,home_page_url,link,score,Category,'',html_text])
                  else:
                      print('already exists')
                      link=''
                      home_page_url=''
                      vendor=''              
              link=''
              home_page_url=''
              vendor=''
      else:
          namevendor=group_vendors
          name=re.sub("[^a-zA-Z0-9]","",str(namevendor))
          for k in search(name+'product', num=3,stop=1, pause=2):
              link=k
          print(namevendor,link)
          home_url = urlparse(link)
          home_page_url= '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
          tsd, td, tsu = extract(home_page_url)
          vendor=td
          if vendor not in vendors_list:
                  finaltext,flag,html_text = scrap_html(home_page_url,vendor)
                  if flag==True:
                      score,Category=find_score(finaltext)
                  else:
                      score=0
                      Category="not founded"
                  csv_writer.writerow([vendor,home_page_url, link,score,Category,'',html_text])
          else:
              print('already exists')
              link=''
              home_page_url=''
              vendor=''
          link=''
          home_page_url=''
          vendor=''            
csv_file.close()
#---------------------------------------------------------------------------
#           sort the csv file based on score
#---------------------------------------------------------------------------

df = pd.read_csv('vendors_webcontent.csv')
df.sort_values(["score"], axis=0, 
                 ascending=False, inplace=True) 
df=df[['vendor','Homepage','link','score','Category','userfeedback']]
df.to_csv('vendors_webcontent_sorted.csv', index=False)
with open('vendors_webcontent_sorted.csv','r') as f, open('vendors_webcontent_sorted_final.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
    
#---------------------------------------------------------------------------
#           cleaning data for  neural network
#---------------------------------------------------------------------------
with open('vendors_webcontent.csv','r') as f, open('vendors_webcontent_2.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
train_data=[]
data=pd.read_csv('vendors_webcontent_2.csv')
data = data[pd.notnull(data['Category'])]
data=data[data.Category != 'not founded']  
data=data[data.html_text!='           ']
data['html_text'].replace(r'^\s*$', np.nan, inplace=True)
data.dropna(subset=['html_text'], inplace=True)
 
#---------------------------------------------------------------------------
#           create a dictionary of DATA against its class
#---------------------------------------------------------------------------
for index,row in data.iterrows():
    train_data.append({"class":row["Category"], "sentence":row["html_text"]})
#---------------------------------------------------------------------------
#          create a list of words across all strings
#---------------------------------------------------------------------------
words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our training data
for pattern in train_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
stemmer = LancasterStemmer()
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)

#---------------------------------------------------------------------------
#         create a list of tokenized words for the pattern
#---------------------------------------------------------------------------
# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

print ("# words", len(words))
print ("# classes", len(classes))    

#---------------------------------------------------------------------------
#         Sigmoid function
#---------------------------------------------------------------------------
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)

#---------------------------------------------------------------------------
#         Cleaning function
#---------------------------------------------------------------------------
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

#---------------------------------------------------------------------------
#        Bag Of Words function
#---------------------------------------------------------------------------
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

#---------------------------------------------------------------------------
#           think function
#---------------------------------------------------------------------------
def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2
#---------------------------------------------------------------------------
#   train one layer with 50000 epochs Neural Network with Logistic regression
#---------------------------------------------------------------------------

def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
    print ("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X),len(X[0]),1, len(classes)) )
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)
        
    for j in iter(range(epochs+1)):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
                
        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) )
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error )
                break
                
        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
        
        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
        
        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))        
        
        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update
        
        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
              }
    synapse_file = "synapses.json"

    with open(synapse_file,'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)
    print ("saved synapses to:", synapse_file)
#---------------------------------------------------------------------------
#           train model
#---------------------------------------------------------------------------

X = np.array(training)
y = np.array(output)

start_time = time.time()

train(X, y, hidden_neurons=10, alpha=0.1, epochs=50000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print ("processing time:", elapsed_time, "seconds")

#---------------------------------------------------------------------------
#           test model
#---------------------------------------------------------------------------
ERROR_THRESHOLD=0.2
synapse_file= 'synapses.json'
with open (synapse_file) as data_file:
    synapse=json.load(data_file)
    synapse_0= np.asarray(synapse['synapse0'])
    synapse_1= np.asarray(synapse['synapse1'])

def classify(sentence , show_details=False):
    results=think(sentence ,show_details)
    results= [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x:x[1], reverse=True)
    return_results=[[classes[r[0]],r[1]] for r in results]
    return return_results
#---------------------------------------------------------------------------
#           google_search result
#---------------------------------------------------------------------------

csv_file = open('vendors_webcontent_test.csv', 'w+', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['vendor','Homepage','link','score','Category','userfeedback','html_text'])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
vendors_list=[]

with open('uniqe_links.txt','r') as input_file:
    for line in input_file:
        home_url = urlparse(line)
        home_page_url= '{uri.scheme}://{uri.netloc}/'.format(uri=home_url)
        tsd, td, tsu = extract(home_page_url)
        vendor=td
        print(vendor,home_page_url)
        for k in search(vendor+'product', num=3,stop=1, pause=2):
              link=k
        if vendor not in vendors_list:
            finaltext,flag,html_text = scrap_html(home_page_url,vendor)
            if flag==True:
                      score,Category=find_score(finaltext)
            else:
                      score=0
                      Category="not founded"
            csv_writer.writerow([vendor,home_page_url, link,score,Category,'',html_text])
        else:
              print('already exists')
              link=''
              home_page_url=''
              vendor=''
        link=''
        home_page_url=''
        vendor=''
csv_file.close()
#---------------------------------------------------------------------------
#           sort the csv file based on score
#---------------------------------------------------------------------------

df = pd.read_csv('vendors_webcontent_test.csv')
df.sort_values(["score"], axis=0, 
                 ascending=False, inplace=True) 
df=df[['vendor','Homepage','link','score','Category','userfeedback']]
df.to_csv('vendors_webcontent_test_sorted.csv', index=False)
with open('vendors_webcontent_test_sorted.csv','r') as f, open('vendors_webcontent_test_sorted_final.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
    
#---------------------------------------------------------------------------
#           cleaning data for  neural network
#---------------------------------------------------------------------------
with open('vendors_webcontent_test.csv','r') as f, open('vendors_webcontent_test_2.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
train_data=[]
data=pd.read_csv('vendors_webcontent_test_2.csv')
data = data[pd.notnull(data['Category'])]
data=data[data.Category != 'not founded']  
data=data[data.html_text!='           ']
data['html_text'].replace(r'^\s*$', np.nan, inplace=True)
data.dropna(subset=['html_text'], inplace=True)
 
