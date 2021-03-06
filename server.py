import random

from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlite3.dbapi2 import Binary
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.datastructure import linked_list
from src.datastructure import hash_table
from src.datastructure import queue
from src.datastructure import stack 
from src.datastructure import binary_search_tree
from src.datastructure import min_heap
from src.models import User, BlogPost, db, app
# app
# app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# db = SQLAlchemy(app)
# now = datetime.now()


# routes
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.address,
                "address": user.address,
                "phone": user.phone
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_user_ll = linked_list.LinkedList()

    for user in users:
        all_user_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )
    
    return jsonify(all_user_ll.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()

    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )
    
    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200



@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "user does not exist!"}), 400

    ht = hash_table.HashTable(10)

    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", datetime.now())
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id"),
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "new blog post created"}), 200


@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })
    
    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"})
    
    return jsonify(post)


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()

    q = queue.Queue()

    for post in blog_posts:
        q.enqueue(post)

    return_list = []

    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(str(char))

        post.data.body = str(numeric_body)

        return_list.append(
            {
                "id": post.data.id,
                "title" : post.data.title,
                "body" : post.data.body,
                "user_id" : post.data.user_id,
            }
        )

    return jsonify(return_list)

@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():
    blog_posts = BlogPost.query.all()

    s = stack.Stack()

    for post in blog_posts:
        s.push(post)

    for _ in range(10):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data)
        db.session.commit()
    
    return jsonify({"message": "success"})



@app.route("/user/min", methods=["GET"])
def get_min_user():
    users = User.query.all()
    user_heap = min_heap.MinHeap()

    keys = []
    for user in users:
        keys.append(user)
    
    user_heap.min_pq(keys)

    min_user = user_heap.min()
    return jsonify(            {
                "id": min_user.id,
                "name": min_user.name,
                "email": min_user.email,
                "address": min_user.address,
                "phone": min_user.phone
            }), 200

if __name__ == "__main__":
    app.run(debug=True)
