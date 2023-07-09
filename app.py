from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Todo, connect_db, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///todos_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def index_page():
    import time
    todos = Todo.query.all() 
    return render_template("index.html", todos=todos, time=time.time())


@app.route("/api/todos")
def list_todos():
    # For every todo in the todo's list, seralize the item
    all_todos = [todo.serialize() for todo in Todo.query.all()]
    return jsonify(todos=all_todos)


@app.route("/api/todos/<int:id>")
def get_todo(id):
    # Seralize a single todo
    todo = Todo.query.get_or_404(id)
    return jsonify(todo=todo.serialize())


@app.route("/api/todos", methods=["POST"])
def create_todo():
    new_todo = Todo(title=request.json["title"])
    db.session.add(new_todo)
    db.session.commit()
    response_json = jsonify(todo=new_todo.serialize())
    return (response_json, 201)


@app.route("/api/todos/<int:id>", methods=["PATCH"])
def update_todo(id):
    todo = Todo.query.get_or_404(id)

    # This is one way of editing a todo
    # If you user tries to edit todo without the proper keys, the app breaks
    # Can update title, can update title and done simultaneously
    # db.session.query(Todo).filter_by(id=id).update(request.json)

    # Another way of changing it
    # Use a .get at the end of the request to make sure we dont set a value as none by accident
    todo.title = request.json.get("title", todo.title)
    todo.done = request.json.get("done", todo.done)

    db.session.commit()
    return jsonify(todo=todo.serialize())


@app.route("/api/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message="deleted")
