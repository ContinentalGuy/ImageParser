import urllib
import requests
import argparse

# Parsing arguments to run programm from command line.
ap = argparse.ArgumentParser()
ap.add_argument('-u','--url', type = str, required = True)
ap.add_argument('-d','--directory', type = str, required = True)
ap.add_argument('-n','--name', type = str, required = True)
ap.add_argument('-r','--Im_range', type = int, required = True)
args = vars(ap.parse_args())

# Links
url = args["url"]
directory = args["directory"]
fname = args["name"]
Im_range = args["Im_range"]
# Creating a request to url.
site = requests.get(str(url))
# Getting content as text.
text = site.text
# List for number of saved images.
pool = []
# Create request to save content by urls
file = urllib.request.URLopener()

for i in range(Im_range):
    name = text.split('\r\n')[i]
    print(name)
    try:
        file.retrieve(name,filename = str(directory)+
                      str(fname)+str(i)+'.jpg')
        pool.append('>  Done')
    except:
        print('|||  Picture was not saved.')
        pass

print('||| Saved: {} pic. from {}.'.format(len(pool),Im_range))
