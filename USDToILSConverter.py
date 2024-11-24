import requests

class USDToILSConverter:
    def __init__(self):
        self.rates = {}  # To store exchange rates with EUR as the base currency

    def fetch_exchange_rates(self):
        """
        Fetches exchange rates for USD, EUR, CHF, and ILS.
        """
        url = 'http://data.fixer.io/api/latest'
        params = {
            'access_key': '63b9eec3e975e61b994ff341ac0ba689',  # Your API Key
            'symbols': 'USD,ILS,EUR,CHF',  # Target currencies
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                self.rates = data.get("rates", {})
                self.rates["EUR"] = 1.0  # Base currency is EUR
                
                # Display conversion of 100 USD to ILS
                usd_to_ils = 100 * (self.rates["ILS"] / self.rates["USD"])
                print(f"Exchange rates fetched: 100 USD = {usd_to_ils:.2f} ILS")
                return True
        print(f"Failed to fetch exchange rates. Error: {response.text}")
        return False

    def convert_to_shekels(self, amount_usd):
        """
        Converts an amount in USD to ILS.
        :param amount_usd: Amount in USD to convert.
        :return: Converted amount in ILS, or None if conversion isn't possible.
        """
        if "ILS" not in self.rates or "USD" not in self.rates:
            print("Exchange rates for USD or ILS are not available.")
            return None
        
        # Convert USD to ILS
        ils_amount = amount_usd * (self.rates["ILS"] / self.rates["USD"])
        return ils_amount


# Main function to demonstrate functionality
def main():
    # Instantiate the USDToILSConverter
    usd_to_ils_converter = USDToILSConverter()

    # Fetch exchange rates
    if usd_to_ils_converter.fetch_exchange_rates():
        while True:
            try:
                # Get user input for amount in USD
                usd_amount = float(input("Enter the amount in Dollars (USD) to convert to Shekels (ILS): "))
                
                # Perform the conversion
                converted_amount = usd_to_ils_converter.convert_to_shekels(usd_amount)
                if converted_amount is not None:
                    print(f"{usd_amount} USD to ILS: {converted_amount:.2f}")

            except ValueError:
                print("Invalid input. Please enter numeric values for the amount.")
            
            # Ask if the user wants another conversion
            another = input("Do you want to perform another conversion? (yes/no): ").strip().lower()
            if another != 'yes':
                print("Goodbye!")
                break
    else:
        print("Failed to fetch exchange rates. Please try again later.")


# Run the program
if __name__ == "__main__":
    main()

