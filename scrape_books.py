import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/'

response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = soup.select('article.product_pod')

    for book in books:
        
        title = book.h3.a['title']
        price = book.select_one('.price_color').text
        print(f'Título: {title} | Preço: {price}')
        
else:
    print(f'Erro ao acessar a página. Status code: {response.status_code}')
