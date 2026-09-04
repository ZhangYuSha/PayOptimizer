# MUBA_Hackathon
A web app that compares transaction fees across payment platforms and card networks (Visa, Mastercard, e-wallets, and more) to recommend the cheapest way to pay. Users can compare costs using payment methods they already own or explore lower-cost alternatives they don't yet have.

# Pay Optimizer — Backend (Person 3)

Simple Flask + SQLite backend for the Pay Optimizer prototype. Provides provider, exchange rate, fee, and user data via a REST API for the frontend (Person 1) and the optimizer logic (Person 2).

This is a **university prototype/demo**, not a production financial application. All exchange rate and fee data is **mock/demo data**.

---

## Requirements

- Python 3.8+
- pip

## Setup

```bash
cd pay-optimizer
pip install -r requirements.txt
```

## Run Order (first time / fresh setup)

Run these **in order** from the `backend/` folder:

```bash
cd backend

# 1. Create the database and tables
python database.py

# 2. Insert demo data (providers, exchange rates, fees)
python seed_data.py

# 3. Start the server
python app.py
```

The server runs at: `http://127.0.0.1:5000`

If you only change code (not the database), you just need step 3 again. Re-run step 2 anytime to reset demo data back to defaults.

---

## Project Structure

```
pay-optimizer/
├── backend/
│   ├── app.py          # Flask app + all API routes
│   ├── database.py     # Creates data.db and the 4 tables
│   ├── seed_data.py     # Inserts demo providers/rates/fees
│   └── data.db          # Created after running database.py (not committed to git)
├── requirements.txt
├── .gitignore
└── README.md
```

`data.db` is **not** committed to GitHub — everyone generates their own local copy by running `database.py` + `seed_data.py`.

---

## API Endpoints

### `GET /api/test`
Health check.

**Response:**
```json
{ "message": "Pay Optimizer backend is working!" }
```

### `GET /api/providers`
List of all providers.

**Response:**
```json
[
  { "id": 1, "name": "Provider A" },
  { "id": 2, "name": "Provider B" }
]
```

### `GET /api/exchange-rates?from=MYR&to=USD`
Exchange rates for a currency pair, across all providers.

**Query params:** `from`, `to` (both required)

**Response:**
```json
[
  { "provider": "Provider A", "rate": 0.234 },
  { "provider": "Provider B", "rate": 0.231 }
]
```

### `GET /api/fees`
Flat fee per provider.

**Response:**
```json
[
  { "provider": "Provider A", "fee": 5 },
  { "provider": "Provider B", "fee": 2 }
]
```

### `GET /api/find-cheapest?from=MYR&to=USD&amount=1000`
Compares all providers for a currency conversion and returns them ranked by amount received, plus the best option and estimated savings.

**Query params:** `from`, `to`, `amount` (all required)

**Response:**
```json
{
  "from_currency": "MYR",
  "to_currency": "USD",
  "amount": 1000.0,
  "options": [
    { "provider": "Provider A", "rate": 0.234, "fee": 5.0, "received": 232.83 },
    { "provider": "Provider B", "rate": 0.231, "fee": 2.0, "received": 230.54 }
  ],
  "best_option": { "provider": "Provider A", "rate": 0.234, "fee": 5.0, "received": 232.83 },
  "estimated_savings": 2.29
}
```

If no exchange rate data exists for the currency pair, `options` is empty and `best_option` is `null` instead of an error:
```json
{
  "from_currency": "MYR",
  "to_currency": "JPY",
  "amount": 1000.0,
  "options": [],
  "best_option": null,
  "estimated_savings": 0
}
```

**Response (400):** `from`, `to`, or `amount` missing, or `amount` is not a number.

### `POST /api/register`
Register a new user. Password is hashed before storage (never stored as plain text).

**Body:**
```json
{ "name": "Test User", "email": "test@example.com", "password": "mypassword" }
```

**Response (201):**
```json
{ "message": "user registered successfully" }
```

**Response (400):** email already registered, or missing fields.

### `POST /api/login`
Log in an existing user.

**Body:**
```json
{ "email": "test@example.com", "password": "mypassword" }
```

**Response (200):**
```json
{ "message": "login successful", "user": { "id": 1, "name": "Test User" } }
```

**Response (401):** invalid email or password.

---

## Demo Data

The seeded data (via `seed_data.py`) is for demonstration only:

- **Provider A** — MYR → USD @ rate 0.234, fee 5 MYR
- **Provider B** — MYR → USD @ rate 0.231, fee 2 MYR

This is **not** real-time financial data.

---

## Notes for Teammates

- **Person 1 (Frontend):** call the `GET` endpoints above directly; CORS is enabled so requests from a different port (e.g. `localhost:3000`) will work.
- **Person 2 (Optimizer):** pull data from `/api/exchange-rates` and `/api/fees`, combine by matching on `provider` name. See `optimizer_example.py` for a working starting template.
- No authentication token/session system yet — login just confirms credentials are valid.