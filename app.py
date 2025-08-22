from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "recipes.db"

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CORS(app)  # right after app creation

@app.route("/")
def home_page():
    return render_template("index.html")


# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------

@app.route("/")
def home():
    return "Hello, Recipe Manager with Persistence!"

# Get all recipes
@app.route("/recipes", methods=["GET"])
def get_recipes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients FROM recipes")
    rows = c.fetchall()
    conn.close()

    recipes = [
        {"id": row[0], "name": row[1], "ingredients": row[2].split(",")}
        for row in rows
    ]
    return jsonify(recipes)

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients FROM recipes WHERE id = ?", (recipe_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Recipe not found"}), 404

    recipe = {"id": row[0], "name": row[1], "ingredients": row[2].split(",")}
    return jsonify(recipe)

# Add a recipe
@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json()

    # Validation
    if not data.get("name") or not isinstance(data.get("name"), str):
        return jsonify({"error": "Recipe name is required and must be a non-empty string"}), 400
    if not data.get("ingredients") or not isinstance(data.get("ingredients"), list):
        return jsonify({"error": "Ingredients must be a non-empty list"}), 400

    ingredients_str = ",".join(data["ingredients"])

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO recipes (name, ingredients) VALUES (?, ?)", (data["name"], ingredients_str))
    conn.commit()
    new_id = c.lastrowid
    conn.close()

    return jsonify({"id": new_id, "name": data["name"], "ingredients": data["ingredients"]}), 201

# Update a recipe
@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,))
    recipe = c.fetchone()
    if not recipe:
        conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    new_name = data.get("name", recipe[1])
    new_ingredients = data.get("ingredients", recipe[2].split(","))
    ingredients_str = ",".join(new_ingredients)

    c.execute("UPDATE recipes SET name=?, ingredients=? WHERE id=?", (new_name, ingredients_str, recipe_id))
    conn.commit()
    conn.close()

    return jsonify({"id": recipe_id, "name": new_name, "ingredients": new_ingredients})

# Delete a recipe
@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,))
    recipe = c.fetchone()
    if not recipe:
        conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    c.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Recipe deleted"})

# Reset recipes (for testing purposes only)
@app.route("/reset", methods=["POST"])
def reset_recipes():
    conn = sqlite3.connect("recipes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes")
    conn.commit()
    conn.close()
    return jsonify({"message": "All recipes cleared"})

# ---------- Run Server ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s port or default 5000
    app.run(host="0.0.0.0", port=port, debug=True)
