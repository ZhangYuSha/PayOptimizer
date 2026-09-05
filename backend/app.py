from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import math
import re

from datetime import datetime, timedelta


app = Flask(__name__)

CORS(app)

DATABASE = "data.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# TEST
# ============================================================

@app.route("/api/test", methods=["GET"])
def test():

    return jsonify({
        "message": "Pay Optimizer backend is working"
    })


# ============================================================
# PROVIDERS
# ============================================================

PROVIDER_CONFIG = {

    "Visa": {
        "base_rate": 0.2325,
        "fee": 8.00,
        "processing_hours": 24
    },

    "Mastercard": {
        "base_rate": 0.2330,
        "fee": 7.00,
        "processing_hours": 24
    },

    "Touch 'n Go": {
        "base_rate": 0.2300,
        "fee": 5.00,
        "processing_hours": 12
    },

    "Wise": {
        "base_rate": 0.2350,
        "fee": 3.50,
        "processing_hours": 12
    },

    "Sui": {
        "base_rate": 0.2340,
        "fee": 0.20,
        "processing_hours": 1
    }
}


@app.route("/api/providers", methods=["GET"])
def providers():

    result = []

    provider_id = 1

    for name in PROVIDER_CONFIG:

        result.append({
            "id": provider_id,
            "name": name
        })

        provider_id += 1

    return jsonify(result)


# ============================================================
# SIMULATED MARKET MODEL
# ============================================================

def simulated_market_rate(
    base_rate,
    hours_from_now
):

    movement = (

        0.0015
        * math.sin(
            hours_from_now / 18
        )

        +

        0.0008
        * math.sin(
            hours_from_now / 7
        )
    )

    return base_rate + movement


# ============================================================
# CALCULATE PROVIDER
# ============================================================

def calculate_provider_option(
    provider_name,
    amount,
    hours_from_now=0
):

    config = PROVIDER_CONFIG[
        provider_name
    ]

    rate = simulated_market_rate(
        config["base_rate"],
        hours_from_now
    )

    fee = config["fee"]

    received = (
        amount - fee
    ) * rate

    return {

        "provider":
            provider_name,

        "rate":
            round(rate, 6),

        "fee":
            round(fee, 2),

        "received":
            round(received, 2),

        "processing_hours":
            config["processing_hours"]
    }


# ============================================================
# EXCHANGE RATES
# ============================================================

@app.route(
    "/api/exchange-rates",
    methods=["GET"]
)
def exchange_rates():

    from_currency = request.args.get(
        "from",
        "MYR"
    )

    to_currency = request.args.get(
        "to",
        "USD"
    )

    if (
        from_currency == to_currency
    ):

        return jsonify({
            provider: 1.0
            for provider in PROVIDER_CONFIG
        })

    if (
        from_currency == "MYR"
        and
        to_currency == "USD"
    ):

        rates = {}

        for provider in PROVIDER_CONFIG:

            option = calculate_provider_option(
                provider,
                1
            )

            rates[
                provider
            ] = option["rate"]

        return jsonify(rates)

    return jsonify({})


# ============================================================
# FEES
# ============================================================

@app.route(
    "/api/fees",
    methods=["GET"]
)
def fees():

    return jsonify({

        provider:
            config["fee"]

        for provider, config
        in PROVIDER_CONFIG.items()

    })


# ============================================================
# FIND CHEAPEST NOW
# ============================================================

@app.route(
    "/api/find-cheapest",
    methods=["GET"]
)
def find_cheapest():

    from_currency = request.args.get(
        "from",
        "MYR"
    )

    to_currency = request.args.get(
        "to",
        "USD"
    )

    try:

        amount = float(
            request.args.get(
                "amount",
                0
            )
        )

    except ValueError:

        return jsonify({
            "error": "Invalid amount"
        }), 400


    if amount <= 0:

        return jsonify({
            "error":
                "amount must be positive"
        }), 400


    if not (
        from_currency == "MYR"
        and
        to_currency == "USD"
    ):

        return jsonify({

            "from_currency":
                from_currency,

            "to_currency":
                to_currency,

            "amount":
                amount,

            "options":
                [],

            "best_option":
                None,

            "estimated_savings":
                0

        })


    options = []

    for provider in PROVIDER_CONFIG:

        option = calculate_provider_option(
            provider,
            amount
        )

        options.append(option)


    options.sort(
        key=lambda x:
            x["received"],
        reverse=True
    )


    best_option = options[0]


    estimated_savings = 0

    if len(options) > 1:

        estimated_savings = (
            best_option["received"]
            -
            options[1]["received"]
        )


    return jsonify({

        "from_currency":
            from_currency,

        "to_currency":
            to_currency,

        "amount":
            amount,

        "options":
            options,

        "best_option":
            best_option,

        "estimated_savings":
            round(
                estimated_savings,
                2
            )

    })


# ============================================================
# DEADLINE OPTIMIZER
# ============================================================

@app.route(
    "/api/optimize-timing",
    methods=["POST"]
)
def optimize_timing():

    data = request.get_json() or {}

    amount = data.get("amount")

    from_currency = data.get(
        "from",
        "MYR"
    )

    to_currency = data.get(
        "to",
        "USD"
    )

    deadline = data.get(
        "deadline"
    )


    if amount is None:

        return jsonify({
            "error":
                "Amount is required."
        }), 400


    if not deadline:

        return jsonify({
            "error":
                "Deadline is required."
        }), 400


    try:

        amount = float(amount)

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "error":
                "Invalid amount."
        }), 400


    try:

        deadline_dt = datetime.fromisoformat(
            deadline
        )

    except ValueError:

        return jsonify({
            "error":
                "Invalid deadline."
        }), 400


    now = datetime.now()


    if deadline_dt <= now:

        return jsonify({
            "error":
                "Deadline must be in the future."
        }), 400


    results = []

    current_time = now


    while current_time <= deadline_dt:

        hours_from_now = (
            current_time - now
        ).total_seconds() / 3600


        for provider in PROVIDER_CONFIG:

            option = calculate_provider_option(
                provider,
                amount,
                hours_from_now
            )


            completion_time = (

                current_time

                +

                timedelta(
                    hours=
                    option[
                        "processing_hours"
                    ]
                )

            )


            # IMPORTANT:
            # Payment must finish before deadline.

            if completion_time <= deadline_dt:

                results.append({

                    "provider":
                        option["provider"],

                    "scheduled_time":
                        current_time.isoformat(
                            timespec="minutes"
                        ),

                    "completion_time":
                        completion_time.isoformat(
                            timespec="minutes"
                        ),

                    "rate":
                        option["rate"],

                    "fee":
                        option["fee"],

                    "received":
                        option["received"],

                    "processing_hours":
                        option[
                            "processing_hours"
                        ]

                })


        current_time += timedelta(
            hours=1
        )


    if not results:

        return jsonify({

            "error":
                "No payment route can complete before the deadline."

        }), 400


    results.sort(

        key=lambda x:
            x["received"],

        reverse=True

    )


    best = results[0]


    safety_buffer = (

        deadline_dt

        -

        datetime.fromisoformat(
            best["completion_time"]
        )

    ).total_seconds() / 3600


    latest_safe_time = (

        deadline_dt

        -

        timedelta(
            hours=
            best["processing_hours"]
        )

    )


    return jsonify({

        "from_currency":
            from_currency,

        "to_currency":
            to_currency,

        "amount":
            amount,

        "deadline":
            deadline_dt.isoformat(
                timespec="minutes"
            ),

        "recommended_provider":
            best["provider"],

        "recommended_time":
            best["scheduled_time"],

        "expected_completion":
            best["completion_time"],

        "expected_received":
            best["received"],

        "exchange_rate":
            best["rate"],

        "fee":
            best["fee"],

        "processing_hours":
            best["processing_hours"],

        "safety_buffer_hours":
            round(
                safety_buffer,
                2
            ),

        "latest_safe_time":
            latest_safe_time.isoformat(
                timespec="minutes"
            ),

        "alternatives":
            results[:10]

    })


# ============================================================
# AI INTENT EXTRACTION
# ============================================================

def extract_payment_intent(message):

    text = message.strip()


    # --------------------------------------------------------
    # AMOUNT
    # --------------------------------------------------------

    amount_match = re.search(

        r"(?:RM|MYR)\s*"
        r"([0-9]+(?:\.[0-9]+)?)",

        text,

        re.IGNORECASE

    )


    if not amount_match:

        amount_match = re.search(

            r"\b"
            r"([0-9]+(?:\.[0-9]+)?)"
            r"\b",

            text

        )


    if not amount_match:

        raise ValueError(
            "I could not determine the payment amount."
        )


    amount = float(
        amount_match.group(1)
    )


    # --------------------------------------------------------
    # TARGET CURRENCY
    # --------------------------------------------------------

    upper_text = text.upper()

    to_currency = "USD"


    if "JPY" in upper_text:

        to_currency = "JPY"

    elif "EUR" in upper_text:

        to_currency = "EUR"

    elif "GBP" in upper_text:

        to_currency = "GBP"


    # --------------------------------------------------------
    # DEADLINE
    # --------------------------------------------------------

    deadline_match = re.search(

        r"(?:by|before)\s+"

        r"(\d{4}-\d{2}-\d{2})"

        r"(?:\s+(\d{1,2}):(\d{2}))?",

        text,

        re.IGNORECASE

    )


    if not deadline_match:

        raise ValueError(

            "Please include a deadline, "
            "for example: "
            "'by 2026-09-15 17:00'."

        )


    date_part = (
        deadline_match.group(1)
    )


    hour = (

        int(deadline_match.group(2))

        if deadline_match.group(2)

        else 23

    )


    minute = (

        int(deadline_match.group(3))

        if deadline_match.group(3)

        else 59

    )


    deadline = datetime.strptime(

        f"{date_part} "
        f"{hour:02d}:"
        f"{minute:02d}",

        "%Y-%m-%d %H:%M"

    )


    return {

        "amount":
            amount,

        "from":
            "MYR",

        "to":
            to_currency,

        "deadline":
            deadline.isoformat()

    }


# ============================================================
# AI OPTIMIZER
# ============================================================

@app.route(
    "/api/ai/optimize",
    methods=["POST"]
)
def ai_optimize():

    data = request.get_json() or {}

    message = data.get(
        "message",
        ""
    ).strip()


    if not message:

        return jsonify({

            "error":
                "Please describe your payment request."

        }), 400


    try:

        intent = extract_payment_intent(
            message
        )

    except ValueError as error:

        return jsonify({
            "error":
                str(error)
        }), 400


    if intent["to"] != "USD":

        return jsonify({

            "intent":
                intent,

            "message":
                (
                    "The request was understood, "
                    "but the current demo optimizer "
                    "supports MYR to USD."
                )

        })


    now = datetime.now()

    deadline_dt = datetime.fromisoformat(
        intent["deadline"]
    )


    results = []

    current_time = now


    while current_time <= deadline_dt:

        hours_from_now = (

            current_time - now

        ).total_seconds() / 3600


        for provider in PROVIDER_CONFIG:

            option = calculate_provider_option(

                provider,

                intent["amount"],

                hours_from_now

            )


            completion_time = (

                current_time

                +

                timedelta(

                    hours=
                    option[
                        "processing_hours"
                    ]

                )

            )


            if completion_time <= deadline_dt:

                results.append({

                    "provider":
                        provider,

                    "scheduled_time":
                        current_time.isoformat(
                            timespec="minutes"
                        ),

                    "completion_time":
                        completion_time.isoformat(
                            timespec="minutes"
                        ),

                    "rate":
                        option["rate"],

                    "fee":
                        option["fee"],

                    "received":
                        option["received"],

                    "processing_hours":
                        option[
                            "processing_hours"
                        ]

                })


        current_time += timedelta(
            hours=1
        )


    if not results:

        return jsonify({

            "error":
                "No payment route can meet the deadline."

        }), 400


    results.sort(

        key=lambda x:
            x["received"],

        reverse=True

    )


    best = results[0]


    seen_providers = set()

    deduped_results = []

    for r in results:

        if r["provider"] not in seen_providers:

            seen_providers.add(r["provider"])

            deduped_results.append(r)


    # --------------------------------------------------------
    # AI-LIKE EXPLANATION
    # --------------------------------------------------------

    reason = (

        f"{best['provider']} provides the "
        f"highest estimated received amount "
        f"while completing before the deadline. "
        f"The estimated processing time is "
        f"{best['processing_hours']} hour(s)."

    )


    return jsonify({

        "intent":
            intent,

        "recommendation": {

            "provider":
                best["provider"],

            "scheduled_time":
                best["scheduled_time"],

            "completion_time":
                best["completion_time"],

            "received":
                best["received"],

            "rate":
                best["rate"],

            "fee":
                best["fee"],

            "processing_hours":
                best["processing_hours"]

        },

        "reason":
            reason,

        "alternatives":
            deduped_results[:5]

    })


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/api/register",
    methods=["POST"]
)
def register():

    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")


    if not name or not email or not password:

        return jsonify({

            "error":
                "All fields are required."

        }), 400


    conn = get_db()


    existing = conn.execute(

        """
        SELECT id
        FROM users
        WHERE email = ?
        """,

        (email,)

    ).fetchone()


    if existing:

        conn.close()

        return jsonify({

            "error":
                "Email already registered."

        }), 409


    hashed_password = generate_password_hash(

        password,

        method="pbkdf2:sha256"

    )


    cursor = conn.execute(

        """
        INSERT INTO users
        (name, email, password)
        VALUES (?, ?, ?)
        """,

        (
            name,
            email,
            hashed_password
        )

    )


    conn.commit()


    user_id = cursor.lastrowid


    conn.close()


    return jsonify({

        "message":
            "Registration successful.",

        "user": {

            "id":
                user_id,

            "name":
                name,

            "email":
                email

        }

    }), 201


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")


    conn = get_db()


    row = conn.execute(

        """
        SELECT *
        FROM users
        WHERE email = ?
        """,

        (email,)

    ).fetchone()


    conn.close()


    if not row:

        return jsonify({

            "error":
                "Invalid email or password."

        }), 401


    if not check_password_hash(

        row["password"],

        password

    ):

        return jsonify({

            "error":
                "Invalid email or password."

        }), 401


    return jsonify({

        "message":
            "login successful",

        "user": {

            "id":
                row["id"],

            "name":
                row["name"],

            "email":
                row["email"]

        }

    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        threaded=True

    )