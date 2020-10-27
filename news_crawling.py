import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
#from urllib.parse import quote
import logging

url_main='https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402&date={date}'
url_base='https://finance.naver.com'

logging.basicConfig(level=logging.INFO)
logging.info('%s crawling', '크롤링중')

#달
def momth():
    date = pd.date_range('2020-09-01', '2020-09-30', freq='D')
    html_date=[]
    for i in date:

        parse_date = (i.strftime('%Y%m%d'))
        html = url_main.format(date=parse_date)

        html_date.append(html)

    return html_date
html_date=momth()



#마지막 페이지 불러오기
def last_page(html):

    page = urlopen(html)
    news_data_soup = BeautifulSoup(page, 'html.parser')

    aa = news_data_soup.find("table", class_='Nnavi').find_all('a')
    link = str(aa[-1]['href'])
    ln = link.split('=')
    last_page = int(ln[-1]) + 1
    return last_page

#last_page=last_page()

#크롤링
def news_data():
    news_title = []
    news_date = []
    news_time = []
    news_site = []
    news_link = []


    for date in range(0,len(html_date)):
        html=html_date[date]

        for i in range(1, last_page(html)):
            url = html + '&page=' + str(i)

            page = urlopen(url)
            news_data_soup = BeautifulSoup(page, 'html.parser')

            news_data_title = news_data_soup.find_all(class_='articleSubject')

            news_data_date = news_data_soup.find_all('span', 'wdate')

            news_data_time = news_data_soup.find_all('span', 'wdate')

            news_data_site = news_data_soup.find_all('span', 'press')

            news_data_link = news_data_soup.find_all(class_='articleSubject')



        for i, j, k, l, m in zip(news_data_title, news_data_date, news_data_time, news_data_site, news_data_link):
            title = i.a.string
            date = j.string.split(' ')[0]
            time = k.string.split(' ')[1]
            site = l.string
            link = m.a['href']
            link=link.replace('§','&sect')

            news_title.append(title)
            news_date.append(date)
            news_time.append(time)
            news_site.append(site)
            news_link.append(url_base+link)

    data = {
        '제목': news_title
        , '링크': news_link
        , '기관': news_site
        , '날짜': news_date
        , '시간': news_time
    }
    news_data = pd.DataFrame(data)

    year=date.split('-')[0]
    month=date.split('-')[1]
    # csv 저장
    news_data.to_csv(
        'D:/big11/data-anal/exam/news/' +year+'년'+ month + '월' + '.csv'
        , sep=','
        , encoding='utf-8'
    )
    return news_data

news_data()




