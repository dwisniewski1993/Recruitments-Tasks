import os

import requests

from PartOne.models import Book
from config import DATABASE, APP_DIR


def initialize_database():
    path = f"{APP_DIR}\\database.db"

    if not os.path.exists(path=path):
        DATABASE.create_all()
        url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'

        req = requests.get(url=url)
        data = req.json()
        books = data["items"]

        for book in books:
            volume = book["volumeInfo"]

            title = volume["title"]

            separator = ";"
            authors = separator.join([f"{author}\n" for author in volume["authors"]])

            published_date = volume["publishedDate"]

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

            image_links = "\n".join([f"{v}" for (k, v) in volume["imageLinks"].items()])
            language = volume["language"]

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
