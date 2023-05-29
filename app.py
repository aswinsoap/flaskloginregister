import sqlite3
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


# Function to create a database connection and initialize the table
def create_connection():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS registrations
                 (name TEXT, email TEXT, password TEXT)"""
    )
    conn.commit()
    conn.close()


# Call the function to create the database connection and initialize the table
create_connection()


@app.route("/")
def home():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Check if password and confirm password match
    if password != confirm_password:
        return "Password and confirm password do not match!"

    # Save the registration data in the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO registrations VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    conn.close()

    # Redirect to the login page
    return redirect(url_for("login"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    # Check if the user is present in the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM registrations WHERE email = ? AND password = ?",
        (email, password),
    )
    user = c.fetchone()
    conn.close()

    if user is None:
        return "Invalid credentials! Please try again."
    else:
        return "Login successful!"


if __name__ == "__main__":
    app.run()
