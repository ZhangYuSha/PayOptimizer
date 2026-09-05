# MUBA_Hackathon
A web app that compares transaction fees across payment platforms and card networks (Visa, Mastercard, e-wallets, and more) to recommend the cheapest way to pay. Users can compare costs using payment methods they already own or explore lower-cost alternatives they don't yet have.

# Pay Optimizer — Backend (Person 3)

Simple Flask + SQLite backend for the Pay Optimizer prototype. Provides provider, exchange rate, fee, and user data via a REST API for the frontend (Person 1) and the optimizer logic (Person 2).

This is a **university prototype/demo**, not a production financial application. All exchange rate and fee data is **mock/demo data**.

---

## Requirements

- Python 3.8+
- pip
- Node.js 20.19+ / 22.12+ and npm (for the `frontend/` Angular app)

## Setup

All commands below are run from the **repository root** (the folder this README is in — there is no `pay-optimizer/` subfolder to `cd` into).

```bash
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

## Running Tests

`requirements.txt` only lists runtime dependencies, so `pytest` isn't installed by the `pip install` step above — install it separately the first time:

```bash
pip install pytest
```

Then, from the repository root:

```bash
pytest test_app.py test_optimizer.py
```

---

## Frontend (Angular)

The Angular app lives in `frontend/`. In a separate terminal, from the repository root:

```bash
cd frontend
npm install
npm start
```

`npm start` runs `ng serve`, available at `http://localhost:4200/`. It calls the backend at `http://127.0.0.1:5000`, so the backend (see **Run Order** above) needs to be running too.

---

## Project Structure

```
./
├── backend/
│   ├── app.py             # Flask app + all API routes
│   ├── database.py        # Creates data.db and the users table
│   ├── seed_data.py       # Inserts demo providers/rates/fees (legacy tables, unused by app.py)
│   └── data.db             # Created after running database.py (not committed to git)
├── frontend/               # Angular app (see Frontend section above)
├── test_app.py             # Backend API tests (pytest)
├── test_optimizer.py       # optimizer_example.py tests (pytest)
├── optimizer_example.py
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
{ "message": "Pay Optimizer backend is working" }
```

### `GET /api/providers`
List of all providers.

**Response:**
```json
[
  { "id": 1, "name": "Visa" },
  { "id": 2, "name": "Mastercard" },
  { "id": 3, "name": "Touch 'n Go" },
  { "id": 4, "name": "Wise" },
  { "id": 5, "name": "Sui" }
]
```

### `GET /api/exchange-rates?from=MYR&to=USD`
Exchange rate per provider for a currency pair, keyed by provider name. `from`/`to` default to `MYR`/`USD` if omitted. Only `MYR` to `USD` currently returns real data; any other pair returns `{}`.

**Response:**
```json
{
  "Visa": 0.2325,
  "Mastercard": 0.233,
  "Touch 'n Go": 0.23,
  "Wise": 0.235,
  "Sui": 0.234
}
```

### `GET /api/fees`
Flat fee per provider, keyed by provider name.

**Response:**
```json
{
  "Visa": 8.0,
  "Mastercard": 7.0,
  "Touch 'n Go": 5.0,
  "Wise": 3.5,
  "Sui": 0.2
}
```

### `GET /api/find-cheapest?from=MYR&to=USD&amount=1000`
Compares all providers for a currency conversion and returns them ranked by amount received, plus the best option and estimated savings. `from`/`to` default to `MYR`/`USD` if omitted.

**Response:**
```json
{
  "from_currency": "MYR",
  "to_currency": "USD",
  "amount": 1000.0,
  "options": [
    { "provider": "Wise", "rate": 0.235, "fee": 3.5, "received": 234.18, "processing_hours": 12 },
    { "provider": "Sui", "rate": 0.234, "fee": 0.2, "received": 233.95, "processing_hours": 1 },
    { "provider": "Mastercard", "rate": 0.233, "fee": 7.0, "received": 231.37, "processing_hours": 24 },
    { "provider": "Visa", "rate": 0.2325, "fee": 8.0, "received": 230.64, "processing_hours": 24 },
    { "provider": "Touch 'n Go", "rate": 0.23, "fee": 5.0, "received": 228.85, "processing_hours": 12 }
  ],
  "best_option": { "provider": "Wise", "rate": 0.235, "fee": 3.5, "received": 234.18, "processing_hours": 12 },
  "estimated_savings": 0.23
}
```

If no exchange rate data exists for the currency pair (i.e. anything other than `MYR` to `USD`), `options` is empty and `best_option` is `null` instead of an error:
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

**Response (400):** `amount` missing, not a number, or not greater than zero.

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

The provider rates/fees returned by the API come from `PROVIDER_CONFIG` in `backend/app.py` (not from the database) and are for demonstration only, MYR → USD:

- **Visa** — rate 0.2325, fee 8.00 MYR, ~24h processing
- **Mastercard** — rate 0.2330, fee 7.00 MYR, ~24h processing
- **Touch 'n Go** — rate 0.2300, fee 5.00 MYR, ~12h processing
- **Wise** — rate 0.2350, fee 3.50 MYR, ~12h processing
- **Sui** — rate 0.2340, fee 0.20 MYR, ~1h processing

Rates fluctuate slightly over time via a simulated market model. This is **not** real-time financial data.

---

## Notes for Teammates

- **Person 1 (Frontend):** call the `GET` endpoints above directly; CORS is enabled so requests from a different port (e.g. `localhost:3000`) will work.
- **Person 2 (Optimizer):** pull data from `/api/exchange-rates` and `/api/fees`, combine by matching on `provider` name. See `optimizer_example.py` for a working starting template.
- No authentication token/session system yet — login just confirms credentials are valid.