from database import get_connection


def seed():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing demo data first, so re-running this script doesn't duplicate rows
    cursor.execute("DELETE FROM exchange_rates")
    cursor.execute("DELETE FROM fees")
    cursor.execute("DELETE FROM providers")

    # Insert providers
    cursor.execute("INSERT INTO providers (name) VALUES ('Provider A')")
    provider_a_id = cursor.lastrowid

    cursor.execute("INSERT INTO providers (name) VALUES ('Provider B')")
    provider_b_id = cursor.lastrowid

    # Insert exchange rates (MYR -> USD)
    cursor.execute(
        "INSERT INTO exchange_rates (provider_id, from_currency, to_currency, rate) VALUES (?, ?, ?, ?)",
        (provider_a_id, "MYR", "USD", 0.234)
    )
    cursor.execute(
        "INSERT INTO exchange_rates (provider_id, from_currency, to_currency, rate) VALUES (?, ?, ?, ?)",
        (provider_b_id, "MYR", "USD", 0.231)
    )

    # Insert fees
    cursor.execute(
        "INSERT INTO fees (provider_id, fee) VALUES (?, ?)",
        (provider_a_id, 5)
    )
    cursor.execute(
        "INSERT INTO fees (provider_id, fee) VALUES (?, ?)",
        (provider_b_id, 2)
    )

    conn.commit()
    conn.close()
    print("Demo data inserted: Provider A and Provider B (MYR -> USD).")


if __name__ == "__main__":
    seed()
