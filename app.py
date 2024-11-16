import sqlite3


def init_db():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS SeasonalFlavors (
            id INTEGER PRIMARY KEY,
            flavor_name TEXT NOT NULL,
            available_until DATE NOT NULL
        )
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Ingredients (
            id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS CustomerFeedback (
            id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            suggestion TEXT,
            allergy_concerns TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/flavors", methods=["GET", "POST"])
def manage_flavors():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    if request.method == "POST":
        flavor_name = request.form["flavor_name"]
        available_until = request.form["available_until"]
        cursor.execute(
            "INSERT INTO SeasonalFlavors (flavor_name, available_until) VALUES (?, ?)",
            (flavor_name, available_until),
        )
        conn.commit()
    cursor.execute("SELECT * FROM SeasonalFlavors")
    flavors = cursor.fetchall()
    conn.close()
    return render_template("manage_flavors.html", flavors=flavors)


@app.route("/inventory", methods=["GET", "POST"])
def manage_inventory():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    if request.method == "POST":
        ingredient_name = request.form["ingredient_name"]
        quantity = request.form["quantity"]
        cursor.execute(
            "INSERT INTO Ingredients (ingredient_name, quantity) VALUES (?, ?)",
            (ingredient_name, quantity),
        )
        conn.commit()
    cursor.execute("SELECT * FROM Ingredients")
    ingredients = cursor.fetchall()
    conn.close()
    return render_template("manage_inventory.html", ingredients=ingredients)


@app.route("/feedback", methods=["POST"])
def submit_feedback():
    customer_name = request.form["customer_name"]
    suggestion = request.form.get("suggestion")
    allergy_concerns = request.form.get("allergy_concerns")
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CustomerFeedback (customer_name, suggestion, allergy_concerns) VALUES (?, ?, ?)",
        (customer_name, suggestion, allergy_concerns),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
