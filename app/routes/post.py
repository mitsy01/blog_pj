from flask import Blueprint, request, render_template, redirect, url_for, flash

from app.db import Session, User, Post
from app.data.password import PASS_SYS_ADM


post_route = Blueprint("posts", __name__)


@post_route.get("/posts/")
@post_route.post("/posts/")
def add_post():
    with Session() as session:
        if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")
            user_id = request.form.get("user_id")
            post = Post(title=title, text=text, user_id=user_id)

            if request.form.get("password") == PASS_SYS_ADM:
                session.add(post)
                session.commit()
                flash("Статтю додано")
            else:
                flash("Невірний пароль")

        users = session.query(User).all()
        return render_template("add_post.html", users=users)


@post_route.get("/post/<int:id>/")
def get_post(id):
    with Session() as session:
        post = session.query(Post).where(Post.id == id).first()
        return render_template("post.html", post=post)


@post_route.get("/")
def index():
    with Session() as session:
        posts = session.query(Post).all()
        return render_template("index.html", posts=posts)


@post_route.get("/post/del/<int:id>/")
def del_post(id):
    with Session() as session:
        post = session.query(Post).where(Post.id == id).first()
        session.delete(post)
        session.commit()
        return redirect(url_for("posts.index"))


@post_route.get("/post/edit/<int:id>/")
@post_route.post("/post/edit/<int:id>/")
def edit_post(id):
    with Session() as session:
        post = session.query(Post).where(Post.id == id).first()
        if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")

            post.title = title
            post.text = text
            session.commit()
            return redirect(url_for("posts.index"))

        return render_template("add_post.html", post=post)