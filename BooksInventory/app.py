from flask import render_template, request, redirect, url_for

from PartOne.models import Book
from PartOne.utils import initialize_database
from config import APP, DATABASE

initialize_database()


# First Part
@APP.route('/')
def all_books():
    return render_template('part_one_first.html', books=Book.query.all())


@APP.route('/results', methods=['POST'])
def searched_books():
    search_string = request.form['searchCondition']
    title_contains_books = Book.query.filter(Book.title.contains(search_string))
    authors_contains_books = Book.query.filter(Book.authors.contains(search_string))
    language_contains_books = Book.query.filter(Book.language.contains(search_string))
    return render_template('part_one_second.html', books=title_contains_books.union_all(authors_contains_books)
                           .union_all(language_contains_books).all())


@APP.route('/add')
def add_book_form():
    return render_template('part_one_third.html')


@APP.route('/adding', methods=['POST'])
def adding_book():
    if request.method == 'POST':
        title = request.form['title']
        authors = ";\n".join(request.form['authors'].split(';'))
        published_date = request.form['publishedDate']

        industry_identifiers = request.form['industryIdentifiers']
        single_identifiers = industry_identifiers.split(';')
        industry_identifiers = ";\n".join([f"{i.split(',')[0]}({i.split(',')[1]})\n" for i in single_identifiers])

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

        return redirect(url_for('all_books'), 302)


if __name__ == '__main__':
    APP.run(debug=True)
