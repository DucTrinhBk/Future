#view-source:https://pasgo.vn/nha-hang/bangkok-thai-cuisine-115-giang-vo-1860
#!/usr/bin/python
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import tensorflow as tf
import ssl
context = ssl._create_unverified_context()
url = 'https://ictnews.vn'
website = urlopen(url, context=context)
html = BeautifulSoup(website.read(), "html.parser")
#open('body.txt','w').write(str(html.find("script", attrs={"crossorigin": "anonymous"}).string))
#print(html.original_encoding)
items = html.find("body").findAll("h4")
for item in items:
    print(item.string)
#print(html.find(id = "gioi-thieu").find(class_='txt-title').string)