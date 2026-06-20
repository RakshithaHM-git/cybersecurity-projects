import random
import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB
)
""")

conn.commit()
conn.close()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 3 or len(password) < 6:
            return "Invalid Input"

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            return "User already exists"

    return render_template("register.html")


# ---------------- LOGIN (STEP 1: PASSWORD CHECK) ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        # PASSWORD CHECK
        if user and bcrypt.checkpw(password.encode("utf-8"), user[2]):

            # 🔐 GENERATE OTP
            otp = str(random.randint(100000, 999999))

            session["otp"] = otp
            session["temp_user"] = username   # temporary until OTP verified

            print("OTP FOR TESTING:", otp)

            return redirect("/verify")

        return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- OTP VERIFY (STEP 2) ----------------
@app.route("/verify", methods=["GET", "POST"])
def verify():

    if request.method == "POST":

        entered_otp = request.form["otp"]

        if entered_otp == session.get("otp"):

            # move user to real session
            session["user"] = session["temp_user"]

            session.pop("otp", None)
            session.pop("temp_user", None)

            return redirect("/dashboard")

        return "Invalid OTP"

    return render_template("verify.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)