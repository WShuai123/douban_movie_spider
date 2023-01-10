import requests
from bs4 import BeautifulSoup

# 爬取到页面源码数据
url = "https://movie.douban.com/subject/4811774/"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}
page_text = requests.get(url,headers=headers).text
soup = BeautifulSoup(page_text,'lxml')

fileDIV = soup.find(attrs={'id': 'info'}).text
print(fileDIV)