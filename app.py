from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)
app.secret_key = "my_super_secret_key_987654"


import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_super_secret_key_987654"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT,
            donation_type TEXT,
            amount TEXT,
            beneficiary TEXT,
            timestamp TEXT,
            previous_hash TEXT,
            current_hash TEXT
        )
    """)
    conn.commit()
    conn.close()

def generate_hash(data, previous_hash):
    return hashlib.sha256((data + previous_hash).encode()).hexdigest()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add_donation():
    if request.method == "POST":
        donor = request.form["donor"]
        dtype = request.form["type"]
        amount = request.form["amount"]
        beneficiary = request.form["beneficiary"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        last = conn.execute("SELECT current_hash FROM donations ORDER BY id DESC LIMIT 1").fetchone()
        prev_hash = last["current_hash"] if last else "0"

        data = donor + dtype + amount + beneficiary + timestamp
        curr_hash = generate_hash(data, prev_hash)

        conn.execute("""
            INSERT INTO donations
            (donor_name, donation_type, amount, beneficiary, timestamp, previous_hash, current_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (donor, dtype, amount, beneficiary, timestamp, prev_hash, curr_hash))

        conn.commit()
        conn.close()

        return f"<h3>Donation Added</h3><p>Transaction Hash:</p><p>{curr_hash}</p><a href='/'>Home</a>"

    return render_template("add.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        tx_hash = request.form["hash"]

        conn = get_db_connection()
        record = conn.execute("SELECT * FROM donations WHERE current_hash = ?", (tx_hash,)).fetchone()
        conn.close()

        if not record:
            return "<h3>Transaction Not Found</h3><a href='/verify'>Try Again</a>"

        data = record["donor_name"] + record["donation_type"] + record["amount"] + record["beneficiary"] + record["timestamp"]
        check_hash = generate_hash(data, record["previous_hash"])

        status = "VERIFIED ✅" if check_hash == record["current_hash"] else "TAMPERED ❌"

        return render_template("result.html", record=record, status=status)

    return render_template("verify.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    total_donations = conn.execute("SELECT COUNT(*) FROM donations").fetchone()[0]

    total_donors = conn.execute(
        "SELECT COUNT(DISTINCT donor_name) FROM donations"
    ).fetchone()[0]

    total_amount = conn.execute(
        "SELECT SUM(CAST(amount AS INTEGER)) FROM donations"
    ).fetchone()[0]

    latest = conn.execute(
        "SELECT * FROM donations ORDER BY id DESC LIMIT 5"
    ).fetchall()

    conn.close()

    if total_amount is None:
        total_amount = 0

    return render_template(
        "dashboard.html",
        total_donations=total_donations,
        total_donors=total_donors,
        total_amount=total_amount,
        latest=latest
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    init_db()
    app.run(debug=True)

