import requests
from bs4 import BeautifulSoup
import json
import re

MAIN_URL = 'https://ppgcc.ufersa.edu.br/'
MAX_NEWS_PAGES_CRAWL = 5 # número máximo de páginas agregadoras de notícias a serem percorridas

def get_soup(url):
    page = requests.get(url)
    # print(f"URL: {url}")
    return BeautifulSoup(page.content, 'html.parser')

def await_news():
    """Percorre até MAX_NEWS_PAGES_CRAWL páginas agregadoras e coleta todas as notícias."""
    all_news = []
    url = MAIN_URL

    for page_num in range(1, MAX_NEWS_PAGES_CRAWL + 1):
        print(f"[INFO] Coletando página {page_num}: {url}")
        page = get_soup(url)
        extract_news_from_page(page, all_news)

        # Busca o link para a próxima página na paginação
        pagination = page.find('ul', class_='pagination')
        next_link_tag = pagination.find('a', class_='next page-numbers') if pagination else None
        if not next_link_tag:
            print('[INFO] Não há próxima página. Encerrando.')
            break
        url = next_link_tag['href']

    # Escreve todas as notícias coletadas em um único arquivo JSON
    with open('news.json', 'w', encoding='utf-8') as file:
        json.dump({'news': all_news}, file, indent=4, ensure_ascii=False)
    print(f"[INFO] Total de notícias coletadas: {len(all_news)}")

    return all_news

def extract_news_from_page(page: BeautifulSoup, all_news: list):
    """Extrai notícias de uma página agregadora e adiciona em `all_news`."""
    container = page.find('div', id='artigos')
    articles = container.find_all('article') if container else []

    for news in articles:
        img = news.find('img')['src'] if news.find('img') else None

        date_elem = news.find('section').find('h5').find_all('small')[-1] if news.find('section') else None
        date = date_elem.get_text(strip=True) if date_elem else None

        title_elem = news.find('h4')
        link = title_elem.find_parent('a')['href'] if title_elem and title_elem.find_parent('a') else None
        title = title_elem.get_text(strip=True) if title_elem else None

        partial_description = news.find('p').get_text(strip=True) if news.find('p') else None

        # Busca e limpa descrição completa
        description_text = None
        if link:
            news_page = get_soup(link)
            desc_section = news_page.find('section', class_='post-body')
            if desc_section:
                for a in desc_section.find_all('a', href=True):
                    href = a['href']
                    prefix = ''
                    prev = a.previous_sibling
                    if isinstance(prev, str):
                        if not prev.endswith((' ', '\n', '\t')):
                            prefix = ' '
                    else:
                        prefix = ' '
                    # a.replace_with(prefix + href)
                    a.replace_with(
                        str(prefix + href).replace('  ',' ')
                    )
                raw_text = desc_section.get_text()                 

                # Normalizações:
                # 1) Múltiplas quebras de linha → única '\n'
                text = re.sub(r"\n+", "\n", raw_text)
                # 2) Remover '\n' no início/final
                text = text.strip('\n')
                # 3) Colapsar múltiplos espaços em apenas um
                text = re.sub(r"[ ]{2,}", " ", text)
                description_text = text

        all_news.append({
            'img': img,
            'date': date,
            'title': title,
            'link': link,
            'partial_description': partial_description,
            'description': description_text
        })

if __name__ == '__main__':
	await_news()