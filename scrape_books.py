import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'

books_data = []
page = 1

os.makedirs('data', exist_ok=True)

while True:
    
    print(f'Processando página {page}...')
    
    url = base_url.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        
        print('Não há mais páginas para processar.')
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.select('article.product_pod')

    for book in books:
        
        title = book.h3.a['title']
        price = book.select_one('.price_color').text

        books_data.append({
            'title': title,
            'price': price
        })

    page += 1

df = pd.DataFrame(books_data)

df.to_csv('data/books.csv', index=False, encoding='utf-8')

print('Scraping finalizado. Arquivo salvo em data/books.csv')
