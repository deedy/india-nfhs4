import requests

URL_LIST = 'state_url_list.txt'
with open(URL_LIST, 'r') as file:
  data = file.readlines()
data = [d.strip() for d in data]

for url in data:
  filename = url[url[:url.rfind("/")].rfind("/")+1:].replace('/', '-')
  res = requests.get(url)
  with open('data_state/' + filename, 'wb') as f:
    f.write(res.content)
