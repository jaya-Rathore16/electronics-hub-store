from flask import Flask, render_template, request, redirect, session
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Admin Login Details
ADMIN_ID = "jaya123"
ADMIN_PASSWORD = "shop2025"

# -------- Database Helper -------- #
def get_products():
    conn = sqlite3.connect("products.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()
    return data

def add_product_to_db(name, description, price, image, category):
    conn = sqlite3.connect("products.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, description, price, image, category) VALUES (?, ?, ?, ?, ?)",
                (name, description, price, image, category))
    conn.commit()
    conn.close()

def update_price(product_id, price):
    conn = sqlite3.connect("products.db")
    cur = conn.cursor()
    cur.execute("UPDATE products SET price=? WHERE id=?", (price, product_id))
    conn.commit()
    conn.close()

# -------- ROUTES -------- #

@app.route("/")
def home():
    products = get_products()
    return render_template("index.html", products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["id"]
        password = request.form["password"]

        if user == ADMIN_ID and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        return render_template("login.html", error="Invalid ID/Password")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")
    products = get_products()
    return render_template("admin.html", products=products)

@app.route("/category/<cat>")
def show_category(cat):
    conn = sqlite3.connect("products.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE category=?", (cat,))
    data = cur.fetchall()
    conn.close()

    return render_template("category.html", products=data, cat=cat)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        price = request.form["price"]
        image_file = request.files["image"]
        category = request.form["category"]


        filename = None
        if image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        add_product_to_db(name, desc, price, filename, category)
        return redirect("/admin")

    return render_template("add_product.html")

@app.route("/update_price", methods=["POST"])
def change_price():
    if "admin" not in session:
        return redirect("/login")

    product_id = request.form["id"]
    price = request.form["price"]
    update_price(product_id, price)
    return redirect("/admin")

@app.route("/delete_product/<int:id>")
def delete_product(id):
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("products.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
