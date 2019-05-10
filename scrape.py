import requests
import time
import os

import pandas as pd
import numpy  as np

from statistics  import mean
from collections import defaultdict
from bs4         import BeautifulSoup as bs

def parse_html(path):

  # Because of varying columns or value descriptions
  # a person is represented as a list where each element 
  # is a tuple. The first value of the tuple coresponds
  # to the index (what will be used as column names later)
  # and the second value corresponds to the actual value
  # of that index.

  person_data = []

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

  table  = soup.find('table', attrs = {'class':'peopleListing'})
  if table is None:
    return None
  
  rows   = table.find_all('tr')
  if rows is None:
    return None

  for row in rows:
    data = row.find_all('td')

    if len(data) != 2:
        continue

    index = data[0].text

    # Occasionally images are provided 
    # as proof of identity. This will 
    # only save the link to that image. 

    if data[1].find('img') is not None:
      value = data[1].find('img')['src']
    else:
      value = data[1].text
    
    person_data.append((index, value))

  # People are represented as a dictionary
  # where the key is the website's unique ID
  # and the value is the list of tuples created earlier
  person = {path : person_data}
      
  return person

def save_page(u_id):
      page = requests.get('http://www.vdc-sy.info/index.php/en/details/martyrs/' + u_id)

      with open(u_id + '.html', 'w+') as file:
        file.write(page.content.decode('utf-8'))

def load_page(path):
    page = bs(open(path, 'html.parser'))
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

def main():
    # files = get_filepaths()

    # for file in files:
    #     person = parse_html(file)

    #     if person not None:

    #     else:
    #         continue

    person = parse_html(os.path.join('pages', '16000.html'))
    print(person)


if __name__ == "__main__":
    main()





