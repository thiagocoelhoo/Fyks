import urllib.request
import re
import json
from zipfile import ZipFile


def update(current_version):
    url = 'https://api.github.com/repos/Rabbithy/Fyks/releases'
    response = urllib.request.urlopen(url)
    data =  json.loads(response.read().decode('utf-8'))
    release = data[0]
    version = re.search('(\d+\.?)+', release['tag_name'])
    
    if version.group() > current_version:
        assets = release['assets']
        download_url = assets[0]['browser_download_url']
        filename, _ = urllib.request.urlretrieve(download_url, filename='../release.zip')
        file = ZipFile(filename, 'r')
        file.extractall('..')
        file.close()
