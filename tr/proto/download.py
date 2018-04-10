
import threading
import requests



def download(link, filelocation):
    r = requests.get(link, stream=True)
    with open(filelocation, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)

def createNewDownloadThread(link, filelocation):
    download_thread = threading.Thread(target=download, args=(link,filelocation))
    download_thread.start()

for i in range(0,5):
    file = "C:\\test" + str(i) + ".png"
    print file
    createNewDownloadThread("http://stackoverflow.com/users/flair/2374517.png", file)

from clint.textui import progress

r = requests.get(url, stream=True)
path = '/some/path/for/file.txt'
with open(path, 'wb') as f:
    total_length = int(r.headers.get('content-length'))
    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
            f.write(chunk)
            f.flush()