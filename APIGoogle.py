
import csv
from googleapiclient.discovery import build
#import requests

api_key = "AIzaSyCI-IG_UDbevc5xyWjuZok7vVi5u8gmtNs"
cse_id = "CYVET"
def google_query(query, api_key, cse_id, **kwargs):
    query_service = build("keysearch", 
                          "v1", 
                          developerKey=api_key
                          )  
    query_results = query_service.cse().list(q=query,    # Query
                                             cx=cse_id,  # CSE ID
                                             **kwargs    
                                             ).execute()
    return query_results['items']
my_results_list = []
keywords=['industrial IOT-youtube','industrial control-youtube','industrial automat-youtube',
     'indutrial IOT certificate-youtube','Industrial Control Systems-youtube', 
      'industrial IOT advisor-youtube']
key=['industrial IOT device-youtube']
for key in keywords:
    my_results = google_query(key,
                          api_key, 
                          cse_id, 
                          num = 10
                          )
    for result in my_results:
        my_results_list.append(result['link'])
        print(result['link'])

csv_file = open('google_search.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow()
csv_writer.writerow(my_results_list)
