import os

import requests
from flask import request

from PartOne.models import Book
from config import DATABASE, APP_DIR


# Additional computations
def initialize_database() -> None:
    """
    Initialize sqlite database of not found any.
    :return: None
    """
    path = f"{APP_DIR}\\database.db"

    if not os.path.exists(path=path):
        DATABASE.create_all()
        url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'

        save_books_to_db(import_books(url=url))


def import_books(url: str) -> dict:
    """
    Sending request to API url and returning given output data.
    :param url: API endpoint
    :return: books dictionary
    """
    req = requests.get(url=url)
    data = req.json()
    books = data["items"]

    return books


def save_books_to_db(books: dict) -> None:
    """
    Saving imported books in dictionary format to sqlite database.
    :param books: dictionary books
    :return: None
    """
    for book in books:
        volume = book["volumeInfo"]

        if "title" in volume:
            title = volume["title"]
        else:
            title = ""

        separator = ";"

        if "authors" in volume:
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
    """
    Adding single book to database.
    :param book: dictionary book
    :return: None
    """
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


def give_all_books(book_obj) -> list:
    """
    Returning list of all books.
    :param book_obj: Database Book model
    :return: dictionary list of book
    """
    return [i.to_dictionary() for i in book_obj.query.all()]


def give_books_by_keyword(book_obj, keyword: str) -> list:
    """
    Returning books filtered by given keyword in title, authors or language columns.
    :param book_obj: Database Book model
    :param keyword: keyword searched in database columns
    :return: dictionary list of book
    """
    title_contains_books = book_obj.query.filter(book_obj.title.contains(keyword))
    authors_contains_books = book_obj.query.filter(book_obj.authors.contains(keyword))
    language_contains_books = book_obj.query.filter(book_obj.language.contains(keyword))
    mass_query = title_contains_books.union_all(authors_contains_books).union_all(language_contains_books).all()
    return [i.to_dictionary() for i in mass_query]


def give_books_by_date(book_obj, start_time: str, stop_time: str) -> list:
    """
    Returning books filtered by given dates.
    :param book_obj: Database Book model
    :param start_time: first time bracket
    :param stop_time: second time bracket
    :return: dictionary list of book
    """
    date_books = book_obj.query.filter(book_obj.publishedDate <= stop_time).filter(book_obj.publishedDate >= start_time)
    return [i.to_dictionary() for i in date_books]
