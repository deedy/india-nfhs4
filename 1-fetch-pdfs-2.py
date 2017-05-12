import requests

URL_LIST = 'url_list2.txt'
with open(URL_LIST, 'r') as file:
  data = file.readlines()
data = [d.strip() for d in data]

for url in data:
  filename = url[url.rfind("/")+1:]
  filename = filename[:filename.find('_')]+'-'+filename[filename.rfind('_')+1:]
  print(filename)
  res = requests.get(url)
  with open('data/' + filename, 'wb') as f:
    f.write(res.content)

