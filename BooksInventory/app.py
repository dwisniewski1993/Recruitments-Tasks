from flask import render_template, request, redirect, url_for, jsonify

from PartOne.models import Book
from config import APP, METHODS
from utils import initialize_database, save_books_to_db, import_books, add_book_to_db, give_all_books, \
    give_books_by_keyword, give_books_by_date

initialize_database()


# First Part
@APP.route('/')
def all_books() -> render_template:
    return render_template('part_one_first.html', books=give_all_books(book_obj=Book))


@APP.route('/results', methods=['POST'])
def searched_books() -> render_template:
    search_string = request.form['searchCondition']
    return render_template('part_one_second.html', books=give_books_by_keyword(book_obj=Book, keyword=search_string))


@APP.route('/filtered', methods=['POST'])
def date_filter() -> render_template:
    dates = request.form
    start_time = dates['startTime']
    stop_time = dates['endTime']
    return render_template('part_one_fourth.html', books=give_books_by_date(book_obj=Book, start_time=start_time,
                                                                            stop_time=stop_time))


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


# Part three
@APP.route('/api/')
def api() -> render_template:
    return render_template('api.html')


@APP.route('/api/books/', methods=METHODS)
def api_books() -> jsonify:
    try:
        if request.method == 'GET':
            option = request.args.get('show_books', 0, type=str)
            if option == 'all':
                return jsonify(result=give_all_books(book_obj=Book))
            elif option == 'keyword':
                keyword = request.args.get('keyword', 0, type=str)
                return jsonify(result=give_books_by_keyword(book_obj=Book, keyword=keyword))
            elif option == 'date':
                start_time = request.args.get('start_time', 0, type=str)
                stop_time = request.args.get('stop_time', 0, type=str)
                return jsonify(result=give_books_by_date(book_obj=Book, start_time=start_time, stop_time=stop_time))
        else:
            return jsonify(result='Only GET method is supported here')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    APP.run()
