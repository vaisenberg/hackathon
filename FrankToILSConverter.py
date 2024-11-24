import requests

class CHFConverter:
    def __init__(self):
        self.rates = {}  # To store exchange rates with EUR as the base currency

    def fetch_exchange_rates(self):
        """
        Fetches exchange rates for CHF, USD, EUR, and ILS relative to EUR.
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
                
                # Display conversion of 100 CHF to ILS
                chf_to_ils = 100 * (self.rates["ILS"] / self.rates["CHF"])
                print(f"Exchange rates fetched: 100 CHF = {chf_to_ils:.2f} ILS")
                return True
        print(f"Failed to fetch exchange rates. Error: {response.text}")
        return False

    def convert_to_shekels(self, amount_chf):
        """
        Converts an amount in CHF to ILS.
        :param amount_chf: Amount in CHF to convert.
        :return: Converted amount in ILS, or None if conversion isn't possible.
        """
        if "ILS" not in self.rates or "CHF" not in self.rates:
            print("Currency codes CHF or ILS are not available.")
            return None
        
        # Convert CHF to ILS using the exchange rate
        ils_amount = amount_chf * (self.rates["ILS"] / self.rates["CHF"])
        return ils_amount


# Main Function for User Interaction
def main():
    # Instantiate the converter
    chf_converter = CHFConverter()

    # Fetch exchange rates
    if chf_converter.fetch_exchange_rates():
        while True:
            try:
                # Get user input for the amount in CHF
                chf_amount = float(input("Enter the amount in Swiss Francs (CHF) to convert to Shekels (ILS): "))

                # Perform the conversion
                converted_amount = chf_converter.convert_to_shekels(chf_amount)
                if converted_amount is not None:
                    print(f"{chf_amount} CHF to ILS: {converted_amount:.2f}")

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
