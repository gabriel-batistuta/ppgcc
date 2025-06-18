import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://ppgcc.ufersa.edu.br/'

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def await_news():
    page = get_soup(MAIN_URL)
    seek_info(page)

def seek_info(page:BeautifulSoup):
    news = []
    
    news_map = {
        'tag':'div',
        'id':'artigos'
    }

    articles_container = page.find(news_map['tag'], attrs={'id':news_map['id']})
    articles = articles_container.find_all('article')

    for news in articles:
        img = news.find('img')
        img = img['src']
        date = news.find('section').find('h5').find_all('small')[-1]
        date = date.text
        title = news.find('h4')
        link = title.find_parent('a')['href']
        print(link)
        title = title.text
        partial_description = news.find('p').text
        news_page = get_soup(link)
        description = news_page.find('section', attrs={'class':'post-body'}).text

        print(locals())

        return {
            'img':img,
            'date':date,
            'title':title,
            'link':link,
            'partial_description':partial_description,
            'description': description
        }