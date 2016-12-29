# Load images from google

import argparse
import urllib.request
import re

parser = argparse.ArgumentParser()
parser.add_argument('-p','--path', type = str,
                    help = 'Set the correct path to the images')
parser.add_argument('-d', '--directory', type = str, default = './',
                    help = 'Where to save pictures.')
args = vars(parser.parse_args())

# Elements of request:
# - google search engine;
# - own request;
# - ending to load google image page.
toGoogleSearch = str('https://www.google.ru/search?q=')
tapeRequest = str()
splitted = (args["path"]).split(' ')
for i in range(len(splitted)):
	if i == len(splitted)-1:
		tapeRequest += str(splitted[i])
	else:
		tapeRequest += str(splitted[i])+'+'
ending = str('&tbm=isch')

# Creating request and hiding by the headers to look like user
try:
    url = str(toGoogleSearch) + str(tapeRequest) + str(ending)
    headers = {}
    headers['User-Agent'] = "Browser (Secret Agent 'Puddle'; Bush)"
    request = urllib.request.Request(url, headers = headers)
    response = urllib.request.urlopen(request)
    responseData = response.read()

    pattern = 'src="(http[,s]:.{2}\w*.{0,100})"'
    URLs = re.findall(pattern, str(responseData))
    
    with open('URLs.txt', 'w') as file:
        for link in URLs:
            file.write(str(link)+'\n')
            print(link)
    print('>  Fetching is done.\n-  URLs are saved.\n-  File is closed.')
    
except Exception as e:
    print(str(e))

file = urllib.request.URLopener()
extensions = ['.jpg','.png','.jpeg']
for num,links in enumerate(URLs):
    try:
        file.retrieve(links,
                          filename = str(args["directory"])+
                          str(args["path"])+str(num)+extensions[0])
        print('-  <pic>{} is saved.'.format(extensions[0]))
    except:
        file.retrieve(links,
                          filename = str(args["directory"])+
                          str(args["path"])+str(num)+extensions[1])
        print('-  <pic>{} is saved.'.format(extensions[1]))
