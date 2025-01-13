import requests
from datetime import datetime

class NBPApiCaller:
    BASE_URL = "https://api.nbp.pl/api/exchangerates/rates/A/"

    def __init__(self):
        pass

    def fetch_exchange_rate(self, base_currency: str, quote_currency: str, start_date: datetime, end_date: datetime):
        if end_date > datetime.now():
            raise ValueError(("Invalid selection", "End date cannot be in the future."))
        

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        if base_currency == quote_currency:
            raise ValueError(("Invalid selection", "Base and quote currenty cannot be the same."))

        try:
            exchange_rates = []

            if base_currency == "PLN": # get PLN to xxx
                # swap
                base_currency, quote_currency = quote_currency, base_currency
                base_currency_rates = self.get_currency_rates(base_currency, start_date_str, end_date_str)

                exchange_rates = [{"date": rate["effectiveDate"], "rate": rate["mid"]} for rate in base_currency_rates]
                exchange_rates = self.convert_rates_to_PLN(exchange_rates)

            elif quote_currency == "PLN": # get xxx to PLN
                base_currency_rates = self.get_currency_rates(base_currency, start_date_str, end_date_str)

                exchange_rates = [{"date": rate["effectiveDate"], "rate": rate["mid"]} for rate in base_currency_rates]
            
            else: # get xxx to xxx
                base_currency_rates = self.get_currency_rates(base_currency, start_date_str, end_date_str)
                quote_currency_rates = self.get_currency_rates(quote_currency, start_date_str, end_date_str)

                exchange_rates = self._combine_rates(base_currency_rates, quote_currency_rates)
            
            return exchange_rates
        
        except requests.exceptions.RequestException as e:
            raise
        

    def get_currency_rates(self, base_currency, start_date_str, end_date_str):
        try:
            response = requests.get(
                f"{self.BASE_URL}{base_currency}/{start_date_str}/{end_date_str}/",
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            currency_rates = data["rates"]
            return currency_rates
        except requests.exceptions.RequestException as e:
            raise ConnectionError(("Connection error", "Retrieving response from NBP API failed due to lack of network connection."))


    def _combine_rates(self, base_rates, quote_rates):
        combined_rates = []

        base_rates_dict = {rate["effectiveDate"]: rate["mid"] for rate in base_rates}
        quote_rates_dict = {rate["effectiveDate"]: rate["mid"] for rate in quote_rates}

        for date, base_rate in base_rates_dict.items():
            if date in quote_rates_dict:
                quote_rate = quote_rates_dict[date]
                
                converted_rate = base_rate / quote_rate
                combined_rates.append({"date": date, "rate": converted_rate})
            else:
                print(f"Found rate in {date} for currency 1, but not found for currency 2.")

        return combined_rates
    
    def convert_rates_to_PLN(self, rates):
        for entry in rates:
            entry['rate'] = 1 / entry['rate']
        return rates

