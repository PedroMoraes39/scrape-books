import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse

BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
BOOK_BASE = 'http://books.toscrape.com/catalogue/{}'

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

def scrape_books(max_pages=None, max_books=None):
    
    books_data = []
    page = 1

    while True:
        print(f'Processando página {page}...')
        response = requests.get(BASE_URL.format(page))

        if response.status_code != 200:
            print('Não há mais páginas para processar.')
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('article.product_pod')

        for book in books:
            if max_books and len(books_data) >= max_books:
                return books_data

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

        if max_pages and page > max_pages:
            print(f'Limite de {max_pages} páginas atingido.')
            break

    return books_data

def main():
    parser = argparse.ArgumentParser(description='Web Scraper para books.toscrape.com')
    parser.add_argument('--save', action='store_true', help='Salvar resultado em CSV')
    parser.add_argument('--output', type=str, default='data/books.csv', help='Caminho para o CSV de saída')
    parser.add_argument('--preview', type=int, nargs='?', const=10, help='Mostra N livros rapidamente (padrão: 10)')
    parser.add_argument('--max-pages', type=int, help='Limita o número máximo de páginas a processar')

    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if args.preview:
        books_data = scrape_books(max_books=args.preview)
        df = pd.DataFrame(books_data)
        print('\nPré-visualização:')
        print(df.to_string(index=False))
        return

    books_data = scrape_books(max_pages=args.max_pages)
    df = pd.DataFrame(books_data)

    if args.save:
        df.to_csv(args.output, index=False, encoding='utf-8')
        print(f'\nArquivo salvo em: {args.output}')

if __name__ == '__main__':
    main()
