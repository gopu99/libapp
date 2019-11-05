from flask import Flask, render_template, request, redirect, url_for
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://libapp:libapp123@localhost/libappdev'
# db = SQLAlchemy(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


class Book(db.Model):
    def __init__(self, data):
        self.title = data[0]
        self.author = data[1]

    title = db.Column(db.String(80),
                      unique=True,
                      nullable=False,
                      primary_key=True)
    author = db.Column(db.String(80),
                       unique=True,
                       nullable=False,
                       primary_key=True)

    def __repr__(self):
        return "<Title: {}, Author: {}>".format(self.title, self.author)


@app.route("/", methods=["GET", "POST"])
def home():
    # books = Book.query.all()
    query = text("SELECT * FROM book")
    books = [Book(data) for data in db.engine.execute(query)]
    return render_template("home.html", books=books)


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    book = Book((title, author))
    db.session.add(book)
    db.session.commit()
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    title = request.form.get("title")
    return redirect(url_for("get_book", title=title))


@app.route("/books", methods=["GET"])
def get_book():
    title = request.args.get("title")
    # book = Book.query.filter_by(title=title).first()
    query = text("SELECT * FROM book WHERE title = \"{}\" limit 1".format(title))
    book_tuple = db.engine.execute(query).first()
    book = Book(book_tuple)
    print(book)
    return render_template("book.html", book=book)


@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newauthor = request.form.get("newauthor")
    book = Book.query.filter_by(title=oldtitle).first()
    # book.title = newtitle
    # book.author = newauthor
    # db.session.commit()
    query = text("""UPDATE book
    SET title = \"{}\", author = \"{}\"
    WHERE
    book.title = \"{}\"
    AND book.author = \"{}\"
    """.format(newtitle, newauthor, book.title, book.author))
    db.engine.execute(query)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    # db.session.delete(book)
    # db.session.commit()
    query = text("""
    DELETE FROM book 
    WHERE book.title = \"{}\" AND book.author = \"{}\"
    """.format(book.title, book.author))
    db.engine.execute(query)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
