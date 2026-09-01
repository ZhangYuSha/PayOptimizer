from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, jsonify, request
from database import get_connection

app = Flask(__name__)


@app.route("/api/test")
def test():
    return jsonify({"message": "Pay Optimizer backend is working!"})


@app.route("/api/providers")
def get_providers():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM providers").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/exchange-rates")
def get_exchange_rates():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")

    conn = get_connection()
    query = """
        SELECT providers.name AS provider, exchange_rates.rate
        FROM exchange_rates
        JOIN providers ON exchange_rates.provider_id = providers.id
        WHERE exchange_rates.from_currency = ? AND exchange_rates.to_currency = ?
    """
    rows = conn.execute(query, (from_currency, to_currency)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/fees")
def get_fees():
    conn = get_connection()
    query = """
        SELECT providers.name AS provider, fees.fee
        FROM fees
        JOIN providers ON fees.provider_id = providers.id
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"error": "email already registered"}), 400

    conn.close()
    return jsonify({"message": "user registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if row is None or not check_password_hash(row["password"], password):
        return jsonify({"error": "invalid email or password"}), 401

    return jsonify({"message": "login successful", "user": {"id": row["id"], "name": row["name"]}})


if __name__ == "__main__":
    app.run(debug=True)
