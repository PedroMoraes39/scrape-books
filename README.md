# 📚 Book Scraper

Um scraper simples feito com Python e BeautifulSoup que extrai dados de livros do site [Books to Scrape](http://books.toscrape.com).  
Permite salvar os dados em CSV ou visualizar os livros diretamente no terminal via linha de comando.

---

## 🚀 Funcionalidades

- Coleta título, preço, avaliação, estoque, categoria e link de cada livro
- Opção de salvar os dados em arquivo CSV
- Pré-visualização rápida de N livros
- Limitação de páginas ou quantidade de livros processados

---

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/book-scraper.git
   cd book-scraper

## 🧪 Uso
▶️ Pré-visualizar os 10 primeiros livros:
   ```bash
   python scrape_books.py --preview
   ```
    
▶️ Pré-visualizar os 5 primeiros livros:
   ```bash
   python scrape_books.py --preview 5
   ```
💾 Salvar todos os livros em CSV:
   ```bash
   python scrape_books.py --save
   ```
💾 Salvar até 3 páginas em CSV:
   ```bash
   python scrape_books.py --save --max-pages 3
   ```
💾 Salvar com nome de arquivo customizado:
   ```bash
   python scrape_books.py --save --output data/meus_livros.csv
   ```