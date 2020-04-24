import os
import requests
import shutil
import hashlib

def compute_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
#        print("{}: {}".format(filename, sha256_hash.hexdigest()))
    return sha256_hash.hexdigest()


def download_book(url, bookname, data_frame, excel_filename, row, excel_sha256_column_name):
    if not os.path.exists(bookname) or \
                  data_frame.at[row, excel_sha256_column_name] != compute_sha256(bookname):
        with requests.get(url, stream = True) as req:
            with open(bookname.encode('utf-8'), 'wb') as out_file:
                shutil.copyfileobj(req.raw, out_file)
            sha256 = compute_sha256(bookname)
            data_frame.at[row, excel_sha256_column_name] = sha256
            try:
                data_frame.to_excel(excel_filename)
            except IOError as e:
                print("\n{}\nPlease close the Excel file before re-running this script.".format(e))
                exit(-1)
    else: print("Not downloading {}".format(bookname))


def compose_bookname(title, author, edition, isbn):
    bookname = title + " - " + author + ", " + edition + " - " + isbn
    if(len(bookname) > 145):
        bookname = title + " - " + author.split(',')[0] + " et al., " + edition + " - " + isbn
    if(len(bookname) > 145):
        bookname = title + " - " + author.split(',')[0] + " et al. - " + isbn
    if(len(bookname) > 145):
        bookname = title + " - " + isbn
    if(len(bookname) > 145):
        bookname = isbn
    return bookname.encode('ascii', 'ignore').decode('ascii')