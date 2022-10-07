from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLAlchemy config
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://opvtxqswlcgjvs:cb425c748e0dc47a02c4569133cd8808c862b14019ba9e763b190a9f0f253e5b@ec2-3-93-206-109.compute-1.amazonaws.com:5432/d6gtmdbdi5bmhf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# SQLAlchemy Todo schema
class Todo(db.Model):
    __tablename__ = "todo"

    # id, title, and complete columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    # Constructor function
    def __init__(self, title, complete):
        self.title = title
        self.complete = complete


# Home function to fetch todo_list from db
@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


# POST end point for creating new todos
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title, False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


# Update function to change todo completion status
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


# Delete function to delete the todo from the db
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
