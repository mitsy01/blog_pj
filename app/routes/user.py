from flask import Blueprint, render_template, request

from app.db import Base, Session, User, Position
from app.data.password import PASS_SYS_ADM

user_route = Blueprint("users", __name__, url_prefix="/users/")


@user_route.get("/")
@user_route.post("/")
def add_user():
    block = False
    msg = ""
    with Session() as session:
        if request.method == "POST":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            position_id = request.form.get("position_id")
            
            if request.form.get("password") == PASS_SYS_ADM:
                user = User(first_name=first_name, last_name=last_name, position_id=position_id)
                session.add(user)
                session.commit()
                msg = "Користувача додано"
            else:
                block = True
                
        positions = session.query(Position).all()
        context = {
            "positions": positions,
            "block": block,
            "msg": msg
        }
        return render_template("user.html", **context)