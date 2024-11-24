import requests

class ILSConverter:
    def __init__(self):
        self.rates = {}  # To store exchange rates with EUR as the base currency

    def fetch_exchange_rates(self):
        """
        Fetches exchange rates for USD, EUR, and CHF relative to ILS.
        """
        url = 'http://data.fixer.io/api/latest'
        params = {
            'access_key': '63b9eec3e975e61b994ff341ac0ba689',  # Your API Key
            'symbols': 'USD,ILS,CHF,EUR',  # Target currencies
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                self.rates = data.get("rates", {})
                self.rates["EUR"] = 1.0  # Base currency is EUR
                
                # Display conversion of 100 ILS to USD, EUR, and CHF
                ils_to_eur = 100 / self.rates["ILS"]
                print(f"Exchange rates fetched: 100 ILS = {ils_to_eur * self.rates['USD']:.2f} USD, "
                      f"{ils_to_eur * self.rates['EUR']:.2f} EUR, "
                      f"{ils_to_eur * self.rates['CHF']:.2f} CHF")
                return True
        print(f"Failed to fetch exchange rates. Error: {response.text}")
        return False

    def convert_to(self, amount_ils, target_currency):
        """
        Converts an amount in ILS to the target currency (USD, EUR, CHF).
        :param amount_ils: Amount in ILS to convert.
        :param target_currency: The target currency (USD, EUR, CHF).
        :return: Converted amount, or None if conversion isn't possible.
        """
        if "ILS" not in self.rates or target_currency not in self.rates:
            print(f"Currency codes ILS or {target_currency} are not available.")
            return None
        
        # Convert ILS to EUR (base currency)
        eur_amount = amount_ils / self.rates["ILS"]
        # Convert EUR to the target currency
        converted_amount = eur_amount * self.rates[target_currency]
        return converted_amount


# Main Function for User Interaction
def main():
    # Instantiate the converter
    ils_converter = ILSConverter()

    # Fetch exchange rates
    if ils_converter.fetch_exchange_rates():
        while True:
            try:
                # Get user input for amount and target currency
                ils_amount = float(input("Enter the amount in Shekels (ILS) to convert: "))
                target_currency = input("Enter the target currency (USD, EUR, CHF): ").strip().upper()

                if target_currency not in ["USD", "EUR", "CHF"]:
                    print("Invalid currency. Please choose USD, EUR, or CHF.")
                    continue

                # Perform the conversion
                converted_amount = ils_converter.convert_to(ils_amount, target_currency)
                if converted_amount is not None:
                    print(f"{ils_amount} ILS to {target_currency}: {converted_amount:.2f}")

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



