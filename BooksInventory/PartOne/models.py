from config import DATABASE


class Book(DATABASE.Model):
    __tablename__ = 'books'
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    title = DATABASE.Column(DATABASE.String(60))
    authors = DATABASE.Column(DATABASE.String(100))
    publishedDate = DATABASE.Column(DATABASE.String(10))
    industryIdentifiers = DATABASE.Column(DATABASE.String())
    pageCount = DATABASE.Column(DATABASE.Integer())
    imageLinks = DATABASE.Column(DATABASE.String(60))
    language = DATABASE.Column(DATABASE.String(60))
