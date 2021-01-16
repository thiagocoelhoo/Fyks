import urllib.request
import re
import json
from zipfile import ZipFile

from app import __version__

releases_url = 'https://api.github.com/repos/Rabbithy/Fyks/releases'


def check_updates():
    response = urllib.request.urlopen(releases_url)
    data =  json.loads(response.read().decode('utf-8'))
    release = data[0]
    version = re.search('(\d+\.?)+', release['tag_name'])
    return version.group() > __version__


def update():
    response = urllib.request.urlopen(releases_url)
    data =  json.loads(response.read().decode('utf-8'))
    release = data[0]
    version = re.search('(\d+\.?)+', release['tag_name'])
    
    if version.group() > __version__:
        assets = release['assets']
        download_url = assets[0]['browser_download_url']
        filename, _ = urllib.request.urlretrieve(download_url, filename='../release.zip')
        file = ZipFile(filename, 'r')
        file.extractall('..')
        file.close()
