import os
import requests
import shutil
import hashlib
import time
import re


def getSHA256(txt):
    """
    Return a valid SHA256 in hexadecimal form (in string type). Otherwise
    return None.
    """
    r = re.search("^[0-9a-fA-F]{64}$", txt)
    if(r == None):
        return None
    return r.string


def compute_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
#        print("{}: {}".format(filename, sha256_hash.hexdigest()))
    return sha256_hash.hexdigest()

def create_relative_path_if_not_exist(relative_path):
    path = os.path.join(os.getcwd(), relative_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def download_book(url, bookname, data_frame, excel_filename, row, sha256_column):
    sha256 = getSHA256(data_frame.at[row, sha256_column])
    print("*** SHA256: {}".format(sha256))
    if os.path.exists(bookname):
      print("+++ SHA256: {}".format(compute_sha256(bookname)))
    if not os.path.exists(bookname) or sha256 != compute_sha256(bookname):
        with requests.get(url, stream = True) as req:
            path = create_relative_path_if_not_exist('tmp')
            tmp_file = os.path.join(path, '_-_temp_file_-_.bak')
            with open(tmp_file, 'wb') as out_file:
                shutil.copyfileobj(req.raw, out_file)
                out_file.close()
            shutil.move(tmp_file, bookname)
            print("--- SHA256: {}".format(compute_sha256(bookname)))
            data_frame.at[row, sha256_column] = compute_sha256(bookname)
            try:
                data_frame.to_excel(excel_filename)
            except IOError as e:
                if str(e).find("Permission denied") >= 0:
                    print("{}\nPlease close the Excel file before re-running this script.".format(e))
                os.remove(bookname)
                exit(-1)
    else: print("Not downloading {}".format(bookname))


replacements = {'/':'-', '\\':'-', ':':'-', '*':'', '>':'', '<':'', '?':'', \
                '|':'', '"':''}


def compose_bookname(title, author, edition, isbn):
    bookname = title + ' - ' + author + ', ' + edition + ' - ' + isbn
    if(len(bookname) > 145):
        bookname = title + ' - ' + author.split(',')[0] + ' et al., ' + \
                    edition + ' - ' + isbn
    if(len(bookname) > 145):
        bookname = title + ' - ' + author.split(',')[0] + ' et al. - ' + isbn
    if(len(bookname) > 145):
        bookname = title + ' - ' + isbn
    if(len(bookname) > 145):
        bookname = title[:130] + ' - ' +isbn
    bookname = bookname.encode('ascii', 'ignore').decode('ascii')
    return "".join([replacements.get(c, c) for c in bookname])