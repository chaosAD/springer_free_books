#!/usr/bin/env python

import os
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from helper import *

folder = create_relative_path_if_not_exist('downloads')

table_url = 'https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4'
table = 'table_' + table_url.split('/')[-1] + '.xlsx'
table_path = os.path.join(folder, table)
if not os.path.exists(table_path):
    books = pd.read_excel(table_url)
    # Create new columns
    books['PDF SHA256'] = '-'
    books['EPUB SHA256'] = '-'
    # Save table
    books.to_excel(table_path)
else:
    books = pd.read_excel(table_path, index_col=0, header=0)


indices_array = np.arange(0, len(books.index))
for row, url, title, author, edition, isbn, category in                     \
                   tqdm(np.c_[indices_array, books[['OpenURL',              \
                                                    'Book Title',           \
                                                    'Author',               \
                                                    'Edition',              \
                                                    'Electronic ISBN',      \
                                                    'English Package Name'  \
                                                    ]].values]):
    new_folder = create_relative_path_if_not_exist(os.path.join(folder, category))

    r = requests.get(url)
    new_url = r.url.replace('%2F','/').replace('/book/','/content/pdf/') + '.pdf'
    bookname = compose_bookname(title, author, edition, isbn)
    output_file = os.path.join(new_folder, bookname + '.pdf')
    print("file: {}".format(output_file.encode('ascii', 'ignore').decode('ascii')))
    download_book(new_url, output_file, books, os.path.join(folder, table), row, 'PDF SHA256')

    # Download EPUB version too if exists
    new_url = r.url.replace('%2F','/').replace('/book/','/download/epub/') + '.epub'
    output_file = os.path.join(new_folder, bookname + '.epub')
    print("file: {}".format(output_file.encode('ascii', 'ignore').decode('ascii')))
    request = requests.get(new_url, stream = True)
    if request.status_code == 200:
       download_book(new_url, output_file, books, os.path.join(folder, table), row, 'EPUB SHA256')

print('\nFinish downloading.')
