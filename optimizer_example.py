import requests

API_BASE_URL = "http://127.0.0.1:5000"


def find_cheapest(from_currency, to_currency, amount):
    """
    Compare payment providers for a currency conversion and rank them.

    Args:
        from_currency (str): source currency code, e.g. "MYR"
        to_currency (str): target currency code, e.g. "USD"
        amount (float): amount to convert, in from_currency

    Returns:
        dict: {
            "from_currency": str,
            "to_currency": str,
            "amount": float,
            "options": [
                {"provider": str, "rate": float, "fee": float, "received": float},
                ...
            ],  # sorted best (highest received) to worst; [] if no rate data found
            "best_option": dict or None,
            "estimated_savings": float,  # best received - worst received; 0 if fewer than 2 options
        }
    """
    rates_response = requests.get(
        f"{API_BASE_URL}/api/exchange-rates",
        params={"from": from_currency, "to": to_currency}
    )
    rates = rates_response.json()

    if not rates:
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "options": [],
            "best_option": None,
            "estimated_savings": 0,
        }

    fees_response = requests.get(f"{API_BASE_URL}/api/fees")
    fees = fees_response.json()
    fee_lookup = {f["provider"]: f["fee"] for f in fees}

    options = []
    for r in rates:
        provider = r["provider"]
        rate = r["rate"]
        fee = fee_lookup.get(provider, 0)
        received = round((amount - fee) * rate, 2)
        options.append({"provider": provider, "rate": rate, "fee": fee, "received": received})

    options.sort(key=lambda x: x["received"], reverse=True)

    estimated_savings = round(options[0]["received"] - options[-1]["received"], 2)

    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "options": options,
        "best_option": options[0],
        "estimated_savings": estimated_savings,
    }


if __name__ == "__main__":
    result = find_cheapest("MYR", "USD", 1000)
    print(result)
