import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
BOOK_BASE = 'http://books.toscrape.com/catalogue/{}'

books_data = []
page = 1

os.makedirs('data', exist_ok=True)

def get_rating(book):
    
    rating_classes = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    star_tag = book.find('p', class_='star-rating')
    
    for class_name in star_tag.get('class', []):
        
        if class_name in rating_classes:
            
            return rating_classes[class_name]
        
    return None

while True:
    
    print(f'Processando página {page}...')
    response = requests.get(BASE_URL.format(page))

    if response.status_code != 200:
        
        print('Não há mais páginas para processar.')
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.select('article.product_pod')

    for book in books:
        
        title = book.h3.a['title']
        price = book.select_one('.price_color').text
        rating = get_rating(book)
        partial_link = book.h3.a['href']
        book_link = BOOK_BASE.format(partial_link)

        book_response = requests.get(book_link)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        stock = book_soup.select_one('p.instock.availability').text.strip()

        breadcrumb = book_soup.select('ul.breadcrumb li a')
        category = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else 'Desconhecida'

        books_data.append({
            'title': title,
            'price': price,
            'rating': rating,
            'stock': stock,
            'category': category,
            'link': book_link
        })

    page += 1

df = pd.DataFrame(books_data)
df.to_csv('data/books.csv', index=False, encoding='utf-8')

print('Scraping completo com dados adicionais salvos em data/books.csv')
