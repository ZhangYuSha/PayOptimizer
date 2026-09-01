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


if __name__ == "__main__":
    app.run(debug=True)
