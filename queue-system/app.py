
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


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), unique=True)
    capacity = db.Column(db.Integer)

class TokenBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(100))
    fee_status = db.Column(db.String(20))
    payment_mode = db.Column(db.String(50))
    slot_time = db.Column(db.String(50))



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

@app.route("/book-token.html")
def book_token_page():
    email = session.get("student_email")
    return render_template("book-token.html", email=email)

# @app.route("/success-token.html")
# def success_token():
#     email = session.get("student_email")
#     return render_template("success-token.html", email=email)


@app.route("/set-40")
def set_40():

    slots = Slot.query.all()

    for s in slots:
        s.capacity = 40

    db.session.commit()

    return "All slots set to 40"
 
@app.route("/success-token.html")
def success_token():

    email = session.get("student_email")
    booking = session.get("booking")

    return render_template(
        "success-token.html",
        email=email,
        booking=booking
    )



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

#---------------------Booking API-----------------------#
@app.route("/submit-booking", methods=["POST"])
def submit_booking():

    data = request.get_json()

    slot = data.get("slot")
    fee = data.get("fee")
    payment = data.get("payment")

    email = session.get("student_email")

    if not email:
        return jsonify({"success": False})

    # generate simple token id
    import random
    token_id = "TKN-" + str(random.randint(100,999))

    # store in session
    session["booking"] = {
        "slot": slot,
        "token": token_id,
        "fee": fee,
        "payment": payment
    }

    return jsonify({
        "success": True,
        "redirect": "/success-token.html"
    })

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
    slots = Slot.query.all()

    if not slots:
        slots = [
            Slot(time="9:00 AM - 10:00 AM", capacity=40),
            Slot(time="10:00 AM - 11:00 AM", capacity=40),
            Slot(time="11:00 AM - 12:00 PM", capacity=40),
            Slot(time="12:00 PM - 1:00 PM", capacity=40),
            Slot(time="1:00 PM - 2:00 PM", capacity=40),
            Slot(time="2:00 PM - 3:00 PM", capacity=40),
            Slot(time="3:00 PM - 4:00 PM", capacity=40),
            Slot(time="4:00 PM - 5:00 PM", capacity=40),
        ]
        db.session.add_all(slots)
        db.session.commit()



# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)