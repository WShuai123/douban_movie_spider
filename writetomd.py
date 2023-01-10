from lxml import etree
import requests
import re
from bs4 import BeautifulSoup

# 新建一个md文件来存储爬取的信息
# 使用'w+'模式是因为如果md文件之前就有，则清空内容。防止上次爬取的信息没删。
md = open('./README.md','w+',encoding='utf-8')

# 爬取到页面源码数据
url = "https://movie.douban.com/subject/4811774/"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}
page_text = requests.get(url,headers=headers).text
soup = BeautifulSoup(page_text,'lxml')
# 数据解析
tree = etree.HTML(page_text)

# 海报图片
pic_res = re.compile(r'<div id="mainpic" class="">.*? <img src="(?P<mainpic>.*?)".*? />', re.S)
pic = pic_res.findall(page_text)
# print(''.join(pic))
md.write('<div align=center><img src="%s"></div>' % ''.join(pic))   # 设置markdown中图片居中显示

# 电影名称和年份
li_list=tree.xpath('//*[@id="content"]/h1//text()')
name = li_list[1]
year = li_list[3]
print(name,year)
md.write(name + year + '<br>')
# 豆瓣评分
stars = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong//text()')
print('◎豆瓣评分：',''.join(stars))
md.write('◎豆瓣评分：' + ''.join(stars) + '<br>')


jieshao = tree.xpath('//*[@id="info"]')
# 导演
director = jieshao[0].xpath('./span[1]/span[2]//text()')
print('◎导演：',''.join(director))
md.write('◎导演：' + ''.join(director) + '<br>')
# 编剧
writer = jieshao[0].xpath('./span[2]/span[2]//text()')
print('◎编剧：',''.join(writer))
md.write('◎编剧：' + ''.join(director) + '<br>')
# 演员
actors = jieshao[0].xpath('./span[3]/span[2]//text()')
print('◎主演：',''.join(actors))
md.write('◎主演：' + ''.join(actors) + '<br>')
# 类型
type = soup.find_all('span', property='v:genre')
movie_type = ''
for i in type:
    movie_type =  movie_type + i.text + ';'
print('◎类型：', movie_type)
md.write('◎类型：' +  movie_type + '<br>')
# 官方网站
site = jieshao[0].xpath('./a//text()')[0]
print('◎官方网站：', site)
md.write('◎官方网站：' +  site + '<br>')
# 制片国家/地区
obj = re.compile(r'<span class="pl">制片国家/地区:</span> (?P<country>.*?)<br/>', re.S)  # re.S让'.'匹配换行符
result = obj.findall(page_text)
print('◎制片国家/地区：',''.join(result))
md.write('◎制片国家/地区：' + ''.join(result) + '<br>')
# 语言
language = re.findall(r'<span class="pl">语言:</span> (?P<language>.*?)<br/>',page_text)
print('◎语言：',''.join(language))
md.write('◎语言：' + ''.join(language) + '<br>')
# 上映日期
date = soup.find_all('span', property='v:initialReleaseDate')
movie_date = ''
for i in date:
    movie_date =  movie_date + i.text + ';'
print('◎上映日期：', movie_date)
md.write('◎上映日期：' + ''.join( movie_date) + '<br>')
# 片长
time = soup.find_all('span', property='v:runtime')
movie_time = ''
for i in time:
    movie_time =  movie_time + i.text + ';'
print('◎片长：', movie_time)
md.write('◎片长：' + ''.join(movie_time) + '<br>')
# 又名
second_name_re = re.compile(r'<span class="pl">又名:</span> (?P<second_name>.*?)<br/>', re.S)
second_name = second_name_re.findall(page_text)
print('◎又名：',''.join(second_name))
md.write('◎又名：' + ''.join(second_name) + '<br>')
# imdb代码
imdb_re = re.compile(r'<span class="pl">IMDb:</span> (?P<imdb>.*?)<br>', re.S)
imdb = imdb_re.findall(page_text)
print('◎IMDb: ',''.join(imdb))
md.write('◎IMDb: ' + ''.join(imdb)+ '<br>')
# 简介
sum_re = re.compile(r'<span property="v:summary" class="">(?P<summary>.*?)</span>',re.S)
summary = sum_re.findall(page_text)
print('◎剧情简介: ', ''.join(summary).replace(' ',''))     # replace删除字符串内的所有空格。
md.write('◎剧情简介:' + '<br>' +''.join(summary).replace(' ',''))  

md.close()
