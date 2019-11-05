from flask import Flask, render_template, request, redirect, url_for
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://libapp:libapp123@localhost/libappdev'
# db = SQLAlchemy(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Book(db.Model):
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
    if request.form:
        book = Book(title=request.form.get("title"),
                    author=request.form.get("author"))
        db.session.add(book)
        db.session.commit()
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/edit", methods=["POST"])
def edit():
    title = request.form.get("title")
    return redirect(url_for("get_book", title=title))


@app.route("/books", methods=["GET"])
def get_book():
    title = request.args.get("title")
    book = Book.query.filter_by(title=title).first()
    print(book)
    return render_template("book.html", book=book)


@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    newauthor = request.form.get("newauthor")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    book.author = newauthor
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
