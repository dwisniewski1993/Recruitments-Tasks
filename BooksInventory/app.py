from flask import render_template, request, redirect, url_for

from PartOne.models import Book
from config import APP
from utils import initialize_database, save_books_to_db, import_books, add_book_to_db

initialize_database()


# First Part
@APP.route('/')
def all_books() -> render_template:
    return render_template('part_one_first.html', books=Book.query.all())


@APP.route('/results', methods=['POST'])
def searched_books() -> render_template:
    search_string = request.form['searchCondition']
    title_contains_books = Book.query.filter(Book.title.contains(search_string))
    authors_contains_books = Book.query.filter(Book.authors.contains(search_string))
    language_contains_books = Book.query.filter(Book.language.contains(search_string))
    return render_template('part_one_second.html', books=title_contains_books.union_all(authors_contains_books)
                           .union_all(language_contains_books).all())


@APP.route('/add')
def add_book_form() -> render_template:
    return render_template('part_one_third.html')


@APP.route('/adding', methods=['POST'])
def adding_book() -> redirect:
    if request.method == 'POST':
        book = request.form
        add_book_to_db(book=book)

        return redirect(url_for('all_books'), 302)


# Part two
@APP.route('/import')
def import_form() -> render_template:
    return render_template('part_two.html')


@APP.route('/importing', methods=['POST'])
def importing() -> redirect:
    if request.method == 'POST':
        results = request.form
        value = results['value']
        url = ""

        if 'condition' not in results:
            url = f"https://www.googleapis.com/books/v1/volumes?q={value}"
        elif results['condition'] == 'title':
            url = f"https://www.googleapis.com/books/v1/volumes?q={value}+intitle"
        elif results['condition'] == 'author':
            url = f"https://www.googleapis.com/books/v1/volumes?q={value}+inauthor"
        elif results['condition'] == 'publisher':
            url = f"https://www.googleapis.com/books/v1/volumes?q={value}+inpublisher"
        elif results['condition'] == 'subject':
            url = f"https://www.googleapis.com/books/v1/volumes?q={value}+subject"

        save_books_to_db(import_books(url=url))
        return redirect(url_for('all_books'), 302)


if __name__ == '__main__':
    APP.run(debug=True)
