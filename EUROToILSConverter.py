import requests

class EURConverter:
    def __init__(self):
        self.rates = {}  # To store exchange rates with EUR as the base currency

    def fetch_exchange_rates(self):
        """
        Fetches exchange rates for EUR, USD, CHF, and ILS relative to EUR.
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
                
                # Display conversion of 100 EUR to ILS
                print(f"Exchange rates fetched: 100 EUR = {100 * self.rates['ILS']:.2f} ILS")
                return True
        print(f"Failed to fetch exchange rates. Error: {response.text}")
        return False

    def convert_to_shekels(self, amount_eur):
        """
        Converts an amount in EUR to ILS.
        :param amount_eur: Amount in EUR to convert.
        :return: Converted amount in ILS, or None if conversion isn't possible.
        """
        if "ILS" not in self.rates or "EUR" not in self.rates:
            print("Currency codes EUR or ILS are not available.")
            return None
        
        # Convert EUR to ILS directly
        ils_amount = amount_eur * self.rates["ILS"]
        return ils_amount


# Main Function for User Interaction
def main():
    # Instantiate the converter
    eur_converter = EURConverter()

    # Fetch exchange rates
    if eur_converter.fetch_exchange_rates():
        while True:
            try:
                # Get user input for the amount in EUR
                eur_amount = float(input("Enter the amount in Euros (EUR) to convert to Shekels (ILS): "))

                # Perform the conversion
                converted_amount = eur_converter.convert_to_shekels(eur_amount)
                if converted_amount is not None:
                    print(f"{eur_amount} EUR to ILS: {converted_amount:.2f}")

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
