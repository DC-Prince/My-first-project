from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) ->str:
        return f"{self.sNo} - {self.title}"
    


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method=="POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if not title or not desc:
            print("Missing title or description!")
        else:
            print(f"Received: {title} - {desc}")
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)


@app.route("/update/<int:sNo>", methods=["GET", "POST"])
def update(sNo):
    todo = Todo.query.filter_by(sNo=sNo).first()
    
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")

        if title and desc:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect("/")
    
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sNo>")
def delete(sNo):
    todo = Todo.query.filter_by(sNo=sNo).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        print(f"Deleted Todo: {todo}")
    else:
        print(f"Todo with sNo={sNo} not found!")

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True, port=8000)