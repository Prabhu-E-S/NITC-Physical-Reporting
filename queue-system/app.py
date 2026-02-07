
# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # CONFIG
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SECRET_KEY'] = "secret"

# db = SQLAlchemy(app)

# # ---------------- MODELS ---------------- #

# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))

# # ---------------- SERVE LOGIN PAGE ---------------- #

# @app.route("/")
# def home():
#     return render_template("login.html")

# @app.route("/student.html")
# def student_page():
#     return render_template("student.html")

# @app.route("/admin.html")
# def admin_page():
#     return render_template("admin.html")


# # ---------------- LOGIN API ---------------- #

# @app.route("/login", methods=["POST"])
# def login():

#     data = request.get_json()

#     role = data.get("role")
#     email = data.get("email")
#     password = data.get("password")

#     if role == "student":
#         user = Student.query.filter_by(
#             email=email,
#             password=password
#         ).first()

#         if user:
#             return jsonify({"success":True,"redirect":"student.html"})
#         return jsonify({"success":False,"message":"Invalid student login"})

#     if role == "admin":
#         user = Admin.query.filter_by(
#             email=email,
#             password=password
#         ).first()

#         if user:
#             return jsonify({"success":True,"redirect":"admin.html"})
#         return jsonify({"success":False,"message":"Invalid admin login"})

#     return jsonify({"success":False,"message":"Invalid role"})

# # ---------------- INIT DB ---------------- #

# with app.app_context():
#     db.create_all()

#     if not Student.query.first():
#         db.session.add_all([
#             Student(email="krishna@nitc.ac.in",password="kkj@1234"),
#             Student(email="prabhu@nitc.ac.in",password="prabhu@nitc")
#         ])

#     if not Admin.query.first():
#         db.session.add_all([
#             Admin(email="jimmy@nitc.ac.in",password="jimmy@1234")
#         ])

#     db.session.commit()

# # ---------------- RUN ---------------- #

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "secret"

db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# ---------------- PAGE ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/student.html")
def student_page():
    email = session.get("student_email")
    return render_template("student.html", email=email)

@app.route("/admin.html")
def admin_page():
    return render_template("admin.html")

# ---------------- LOGIN API ---------------- #

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    role = data.get("role")
    email = data.get("email").strip()
    password = data.get("password").strip()

    # -------- STUDENT LOGIN -------- #
    if role == "student":
        user = Student.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            session["student_email"] = email   # ⭐ STORE EMAIL
            return jsonify({"success":True,"redirect":"student.html"})

        return jsonify({"success":False,"message":"Invalid student login"})

    # -------- ADMIN LOGIN -------- #
    if role == "admin":
        user = Admin.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            session["admin_email"] = email
            return jsonify({"success":True,"redirect":"admin.html"})

        return jsonify({"success":False,"message":"Invalid admin login"})

    return jsonify({"success":False,"message":"Invalid role"})

# ---------------- INIT DB ---------------- #

with app.app_context():
    db.create_all()

    if not Student.query.first():
        db.session.add_all([
            Student(email="krishna_b250946ec@nitc.ac.in",password="kkj@1234"),
            Student(email="prabhu_b250123cs@nitc.ac.in",password="prabhu@nitc")
        ])

    if not Admin.query.first():
        db.session.add(
            Admin(email="jimmy@nitc.ac.in",password="jimmy@1234")
        )

    db.session.commit()

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
