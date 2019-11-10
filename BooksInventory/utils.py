import os

import requests
from flask import request

from PartOne.models import Book
from config import DATABASE, APP_DIR


def initialize_database() -> None:
    path = f"{APP_DIR}\\database.db"

    if not os.path.exists(path=path):
        DATABASE.create_all()
        url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'

        save_books_to_db(import_books(url=url))


def import_books(url: str) -> dict:
    req = requests.get(url=url)
    data = req.json()
    books = data["items"]

    return books


def save_books_to_db(books: dict) -> None:
    for book in books:
        volume = book["volumeInfo"]

        title = volume["title"]

        separator = ";"
        if "author" in volume:
            authors = separator.join([f"{author}\n" for author in volume["authors"]])
        else:
            authors = ""

        if "publishedDate" in volume:
            published_date = volume["publishedDate"]
        else:
            published_date = ""

        if "industryIdentifiers" in volume:
            industry_identifiers = volume["industryIdentifiers"]
            industry_identifiers = separator.join([f"{i['identifier']}({i['type']})\n"
                                                   for i in industry_identifiers])
        else:
            industry_identifiers = ""

        if "pageCount" in volume:
            page_count = volume["pageCount"]
        else:
            page_count = 0

        if "imageLinks" in volume:
            image_links = "\n".join([f"{v}" for (k, v) in volume["imageLinks"].items()])
        else:
            image_links = ""

        if "language" in volume:
            language = volume["language"]
        else:
            language = ""

        DATABASE.session.add(Book(title=title,
                                  authors=authors,
                                  publishedDate=published_date,
                                  industryIdentifiers=industry_identifiers,
                                  pageCount=page_count,
                                  imageLinks=image_links,
                                  language=language
                                  )
                             )
    DATABASE.session.commit()


def add_book_to_db(book: dict) -> None:
    if "title" in book:
        title = request.form['title']
    else:
        title = ""

    if "authors" in book:
        authors = ";\n".join(request.form['authors'].split(';'))
    else:
        authors = ""

    if "publishedDate" in book:
        published_date = request.form['publishedDate']
    else:
        published_date = ""

    if "" in book:
        industry_identifiers = request.form['industryIdentifiers']
        single_identifiers = industry_identifiers.split(';')
        industry_identifiers = ";\n".join([f"{i.split(',')[0]}({i.split(',')[1]})\n" for i in single_identifiers])
    else:
        industry_identifiers = ""

    page_count = request.form['pageCount']
    links = ";\n".join(request.form['links'].split(','))
    languages = ";\n".join(request.form['languages'].split(','))

    book = Book(title=title,
                authors=authors,
                publishedDate=published_date,
                industryIdentifiers=industry_identifiers,
                pageCount=page_count,
                imageLinks=links,
                language=languages
                )

    DATABASE.session.add(book)
    DATABASE.session.commit()
