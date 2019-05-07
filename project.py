import requests
import pickle
import time
import tqdm
import glob
import os
import re

import pandas as pd
import numpy  as np

from statistics  import mean
from collections import defaultdict
from bs4         import BeautifulSoup as bs

def parse_html(path, uid):

  # Because of varying columns or value descriptions
  # a person is represented as a list where each element 
  # is a tuple. The first value of the tuple coresponds
  # to the index (what will be used as column names later)
  # and the second value corresponds to the actual value
  # of that index.

  person_data = {}
  cols = []
  vals = []

  page   = load_page(path)
  if page is None: 
    return None

  # The HTML pages we have saved from the website are structured 
  # where a table holds all the relevant information we need. As 
  # of May 1, 2019 there are two rows at the top of this table 
  # that contain some unrelated javascript code. The following
  # rows contain only two <td> tags, so we navigate to that level
  # in this html page.
  #
  # Right now the code below works for the specific pages we are 
  # targeting however, this is not foolproof and should be properly
  # tested if using this code in the future.

  table  = page.find('table', attrs = {'class':'peopleListing'})
  if table is None:
    return None
  
  rows   = table.find_all('tr')
  if rows is None:
    return None

  for row in rows:
    data = row.find_all('td')

    if len(data) != 2:
        continue

    cols.append(data[0].text)

    # Occasionally images are provided 
    # as proof of identity. This will 
    # only save the link to that image. 

    if data[1].find('img') is not None:
      vals.append(data[1].find('img')['src'])
    else:
      vals.append(data[1].text)
    

  # People are represented as a dictionary
  # where the key is the website's unique ID
  # and the value is the list of tuples created earlier
  
  cols.append('uid')
  vals.append(uid)

  person = pd.DataFrame([vals], columns = cols, dtype=str)
      
  return person

def save_page(u_id):
  page = requests.get('http://www.vdc-sy.info/index.php/en/details/martyrs/' + u_id)

  with open(u_id + '.html', 'w+') as file:
    file.write(page.content.decode('utf-8'))

def load_page(path):
  with open(path) as fp:
    page = bs(fp, 'html.parser')

  return page

def get_page(url):
  return requests.get(url)

def scrape(unique_ids):
  times = []

  for i in unique_ids:
    time.sleep(1)
    start = time.time()

    try:
        save_page(f'{i:05}')
        print('Saved page: ' + f'{i:05}')

        elapsed = time.time() - start
        times.append(elapsed)

        print('Elapsed Time: ', elapsed)
        print('Average Time: ', (mean(times)))

    except Exception as e:
        print(e)

def formatted_print(person):
  # print(person)
  # pattern = r'[0-9][0-9][0-9][0-9][0-9]'
  # key     = str(next(iter(person)))
  # uid     = re.findall(pattern, key)[0]
  # print(pattern.match(name))
  # # print(name)

  uid = str(person['uid'][0])
  # pad_len = max([len(pair[0]) for pair in person[uid]])
  pad_len = 32

  os.system('clear')
  print('\n==== ID:', uid, '=' * 59)

  vals = person.values[0]
  col_labels = list(person)
  
  for i in range (len(col_labels)):
    print(col_labels[i].ljust(pad_len), ' : ', repr(vals[i]))

  print('=' * 72, '\n')

def get_uID(filename):
  pattern = r'[0-9][0-9][0-9][0-9][0-9]+'
  uid     = re.findall(pattern, filename)[0]
  return str(uid)

def save_person(person):
  uid = str(person['uid'][0])
  pickle.dump(person, open(os.path.join('persons', uid + '.pickle'), 'wb'))

def load_person(filename):
  return pickle.load(open(filename, 'rb'))

def process_HTML():
  num_of_files = len(os.listdir('pages'))
  path         = os.path.join('pages', '*.html')
  counter      = 1
  times        = []
  
  for filename in glob.iglob(path):
    person = parse_html(filename, get_uID(filename))

    if person is None:
      # counter += 1
      continue

    save_person(person)
    os.system('clear')
    print(f'{counter} / {num_of_files} files processed. ')
    counter += 1

def process_dataframes():
  all_df = []
  path   = os.path.join('persons', '*.pickle')

  for filename in glob.iglob(path):
    uid    = get_uID(filename)
    person = load_person(os.path.join('persons', uid + '.pickle'))
    person = rename_dup_cols(person)
    print(filename)
    all_df.append(person)

  save(all_df, 'all_df_list')

def rename_dup_cols(dataframe):
  cols = pd.Series(dataframe.columns)
  for dup in dataframe.columns.get_duplicates(): 
    cols[dataframe.columns.get_loc(dup)] = [dup+'_'+str(d_idx) if d_idx != 0 else dup for d_idx in range(dataframe.columns.get_loc(dup).sum())]
  
  dataframe.columns = cols

  return dataframe

def combine_dataframes(dataframes):
  failed_dataframes = []
  combined = pd.DataFrame()

  current = 0
  num     = len(dataframes)

  for df in dataframes:
    try:
      combined = pd.concat([combined, df], axis = 0)
      print(f'{counter} / {num} people processed in combine_dataframes().')
      counter+=1
    
    except Exception as e:
      failed_dataframes.append(df)
      print('Failed')
      counter+=1

  save(combined, 'all_comb_df')
  save(failed_dataframes, 'failed_df')

  print('\n\nSuccess: ', len(dataframes) - len(failed_dataframes))
  print('Failed: ', len(failed_dataframes))

def save(obj, name):
  pickle.dump(obj, open(name + '.pickle', 'wb'))

def load(name):
  return pickle.load(open(name + '.pickle', 'rb'))

def main():
  # parse_html()
  process_HTML()
  process_dataframes()

  # list_df = load('all_df')

  combine_dataframes(list_df)

if __name__ == "__main__":
  main()





