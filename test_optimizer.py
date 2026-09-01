from unittest.mock import MagicMock, patch

from optimizer_example import find_cheapest


def mock_response(json_data):
    resp = MagicMock()
    resp.json.return_value = json_data
    return resp


def make_side_effect(rates, fees):
    def side_effect(url, params=None):
        if "exchange-rates" in url:
            return mock_response(rates)
        if "fees" in url:
            return mock_response(fees)
        raise AssertionError(f"unexpected URL requested: {url}")
    return side_effect


@patch("optimizer_example.requests.get")
def test_normal_case_computes_estimated_savings(mock_get):
    mock_get.side_effect = make_side_effect(
        rates=[
            {"provider": "Provider A", "rate": 0.234},
            {"provider": "Provider B", "rate": 0.231},
        ],
        fees=[
            {"provider": "Provider A", "fee": 5},
            {"provider": "Provider B", "fee": 2},
        ],
    )

    result = find_cheapest("MYR", "USD", 1000)

    assert result["options"] == [
        {"provider": "Provider A", "rate": 0.234, "fee": 5, "received": 232.83},
        {"provider": "Provider B", "rate": 0.231, "fee": 2, "received": 230.54},
    ]
    assert result["best_option"]["provider"] == "Provider A"
    # 232.83 - 230.54
    assert result["estimated_savings"] == 2.29


@patch("optimizer_example.requests.get")
def test_single_provider_has_zero_savings(mock_get):
    mock_get.side_effect = make_side_effect(
        rates=[{"provider": "Provider A", "rate": 0.234}],
        fees=[{"provider": "Provider A", "fee": 5}],
    )

    result = find_cheapest("MYR", "USD", 1000)

    assert len(result["options"]) == 1
    assert result["best_option"] == result["options"][0]
    # only one option: best and worst are the same, so there's nothing to save
    assert result["estimated_savings"] == 0


@patch("optimizer_example.requests.get")
def test_no_rate_data_returns_empty_structure_without_error(mock_get):
    mock_get.side_effect = make_side_effect(rates=[], fees=[{"provider": "Provider A", "fee": 5}])

    result = find_cheapest("MYR", "JPY", 1000)

    assert result == {
        "from_currency": "MYR",
        "to_currency": "JPY",
        "amount": 1000,
        "options": [],
        "best_option": None,
        "estimated_savings": 0,
    }
    # /api/fees should never be called once /api/exchange-rates comes back empty
    assert mock_get.call_count == 1


@patch("optimizer_example.requests.get")
def test_zero_fee_provider(mock_get):
    mock_get.side_effect = make_side_effect(
        rates=[{"provider": "Provider C", "rate": 0.5}],
        fees=[{"provider": "Provider C", "fee": 0}],
    )

    result = find_cheapest("MYR", "USD", 1000)

    assert result["options"][0]["fee"] == 0
    assert result["options"][0]["received"] == 500.0
    assert result["estimated_savings"] == 0
