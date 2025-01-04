import unittest
from parameterized import parameterized
from nbp_api_caller import NBPApiCaller
from datetime import datetime, timedelta

#  Tests should be ran with
# "python3 -m unittest test.py -v"
#  to print the output in the terminal

class TestNBPApiCaller(unittest.TestCase):
    def setUp(self):
        self.caller = NBPApiCaller()

    @parameterized.expand([
        ("USD", "PLN"),
        ("EUR", "PLN"),
        ("GBP", "PLN"),
        ("USD", "EUR"),
        ("USD", "GBP"),
    ])
    def test_fetch_exchange_rate(self, base_currency, quote_currency):
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        rates = self.caller.fetch_exchange_rate(base_currency, quote_currency, start_date, end_date)
        self.assertIsInstance(rates, list)
        self.assertGreater(len(rates), 0)

    @parameterized.expand([
        ("USD"),
        ("EUR"),
        ("GBP"),
    ])
    def test_get_currency_rates(self, currency):
        start_date_str = "2022-01-01"
        end_date_str = "2022-01-31"
        rates = self.caller.get_currency_rates(currency, start_date_str, end_date_str)
        self.assertIsInstance(rates, list)
        self.assertGreater(len(rates), 0)

    def test_convert_rates_to_pln(self):
        rates = [{"rate": 4.5}, {"rate": 4.6}]
        converted_rates = self.caller.convert_rates_to_PLN(rates)
        self.assertIsInstance(converted_rates, list)
        self.assertEqual(len(converted_rates), 2)
        self.assertAlmostEqual(converted_rates[0]["rate"], 1 / 4.5, places=4)
        self.assertAlmostEqual(converted_rates[1]["rate"], 1 / 4.6, places=4)

    def test_combine_rates(self):
        base_rates = [{"effectiveDate": "2022-01-01", "mid": 4.5},
                      {"effectiveDate": "2022-01-02", "mid": 4.6}]
        quote_rates = [{"effectiveDate": "2022-01-01", "mid": 1.2},
                       {"effectiveDate": "2022-01-03", "mid": 1.3}]
        combined_rates = self.caller._combine_rates(base_rates, quote_rates)
        self.assertIsInstance(combined_rates, list)
        self.assertEqual(len(combined_rates), 1)
        self.assertAlmostEqual(combined_rates[0]["rate"], 4.5 / 1.2, places=4)