import json

# Function to load the JSON data from a file and access specific information
def load_exchange_data(file_name):
    # Open the JSON file
    with open(file_name, 'r') as file:
        # Load the JSON content and convert it to a Python dictionary
        data = json.load(file)
        
    # Return the loaded dictionary
    return data

# Load data from the file
data = load_exchange_data('exchange_rates.json')

# Now you can access the data like a dictionary
# Example: Pretty print the entire dictionary (or just the rates part)
import pprint
pprint.pprint(data['rates'])  # This prints the 'rates' section in a readable format

# Example: Access and print specific information from the dictionary
currency = 'EUR'  # Replace with the currency code you're interested in (e.g., 'USD', 'ILS')
if 'rates' in data and currency in data['rates']:
    print(f"\nExchange rate for 1 EUR to {currency}: {data['rates'][currency]}")
else:
    print(f"Error: {currency} not found in the exchange rates.")
