# Springer E-Books For Free (Yeah! You Read It Right!)
Springer releases e-books for free during this 2020 COVID-19 quarantine period. Download them using this Python script.

**Note**: If you want just one or two specific books, get the excel file [here](https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4) and manually download those or use the script to help you download (see **Download book selectively** sub-section). It took about 4 hours to complete the 409 english books (14 GB, both PDF and EPUB) on my machine.

## TL;DR
1. Clone this project or download the zip file and unzip it to a directory of your choice.
2. The simplest is to run `run_VirtualEnv.bat` file by double-clicking on it from Windows Explorer. All e-books can be found in the `./downloads` subfolder (asumming everything is fine and dandy) and you are done. Read no further than the next word. I am serious!

If you want a finer control of what to download, then instead of doing step 2 above, do the following
1. Unzip the project to `C:\springer\` (or a directory of your choice, but the following steps assume you use my suggestion)
2. Open a `cmd` console and type the following
```
cd springer
setup_env.bat
```
3. Read the next step
4. Since you have reached this far, you must have enjoyed reading. Read on ;-)

## Usage
By default the script stores the books in `./downloads` subfolder according to the subject ("English Package Name" column of the excel file).

### Download all books (PDF and EPUB)
Use the following command to download all PDF and EPUB books to the default download folder `./downloads`
```
python3 main.py
```
Nothing so special about this command because you can achieve the same result by double-clicking on the `run_VirtualEnv.bat`. But, stay with me.

To download them to a subfolder of your choice, say `books`
```
python3 main.py -f ./books
```
You can download to an absolute path, say `C:/ebooks/springer/`
```
python3 main.py -f C:/ebooks/springer/
```

### Download all books of specific format
To download all PDF books only, run
```
python3 main.py --pdf
```
or all EPUB books only
```
python3 main.py --epub
```

### Download only specific book categories
You can download selective books by categories. Make sure category name with space(s) is enclosed in double quotation marks,  like so
```
python3 main.py -c Enginnering "CoMpuTer sciEnCe"
```
The category name is case-insensitive.

### Download book selectively
You can download books by indices (refer to the excel file for the titles)
```
python3 main.py -i 2 345 70 90 0 213
```

### Verbose mode
If you need to know what you are downloading, enable the verbose mode with `-v` option
```
python3 main.py -v -c "Behavioral science and psychology" "chaos AD" UFO "Life science" -i 2 34 400
```
You will get the following summary before the downloading starts
```
                                          Book Title               English Package Name
2                                  All of Statistics         Mathematics and Statistics
34                            Essential Astrophysics              Physics and Astronomy
37       International Perspectives on Psychotherapy  Behavioral Science and Psychology
40                         Applied Behavior Analysis  Behavioral Science and Psychology
70                          Psychology of Perception  Behavioral Science and Psychology
95             Handbook of Consumer Finance Research  Behavioral Science and Psychology
311       Clinical Methods in Medical Family Therapy  Behavioral Science and Psychology
313                           Motivation and Action   Behavioral Science and Psychology
381                          Perceptual Organization  Behavioral Science and Psychology
396  Evidence-Based Practice in Clinical Social Work  Behavioral Science and Psychology
397                 Foundations of Behavioral Health  Behavioral Science and Psychology
398                      Social Psychology in Action  Behavioral Science and Psychology
400             A Course in Rasch Measurement Theory                          Education

13 titles ready to be downloaded...
The following invalid book categories will be ignored:
 1. chaos AD
 2. UFO
 3. Life science
```

## Seting up virtual environment
You can skip this section since it has been done for you by either `run_VirtualEnv.bat` or `setup_env.bat`. If you are reading this part because every else fails, then read on.

So you got problem with auto mode? Try the manual mode below.
### Running in a virtual environment

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Virtual environment on Windows (Python 3.x)

```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

### Virtual environment on Windows (Python 2.7.x)
```
python -m virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements2x.txt
python main.py
```
If you succeed, you might want to revisit the `Usage` section. If you still fail, I can't help you further. Sorry I am just another `README.MD`. Please seek help from some intelligent human.

## Docker container to do all the work
This section is dedicated to Docker fans.

Considering you cloned the repo in a folder, as:
```bash
cd \home\[user]\workspace`
git clone https://github.com/alexgand/springer_free_books.git
cd springer_free_books
mkdir downloads
```

You can run the scripts like that:
```bash
docker build . -t springer-image
docker run --rm -v [local_download_folder]:/app/downloads springer-image
```
and the downloads will be at [`local_download_folder`]

## Source
* https://group.springernature.com/gp/group/media/press-releases/freely-accessible-textbook-initiative-for-educators-and-students/17858180?utm_medium=social&utm_content=organic&utm_source=facebook&utm_campaign=SpringerNature_&sf232256230=1
* https://www.springernature.com/gp/librarians/news-events/all-news-articles/industry-news-initiatives/free-access-to-textbooks-for-institutions-affected-by-coronaviru/17855960
* https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4

Thanks Springer!