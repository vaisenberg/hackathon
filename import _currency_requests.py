import requests
import json  # Import the json module

# URL for Fixer API to get the latest exchange rates
url = 'http://data.fixer.io/api/latest'

# Parameters for the API request
params = {
    'access_key': '63b9eec3e975e61b994ff341ac0ba689',  # Replace with your actual API key
    'base': 'EUR',  # Base currency (EUR)
    'symbols': 'USD,ILS,CHF'  # Currencies we are interested in
}

# Make the GET request to fetch the data
response = requests.get(url, params=params)  # Include the params in the request

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Parse the response JSON

    # Print the entire response data as-is
    print(data)  # This prints the full JSON response

    # If you want to upload this to a database, file, or server, you can save it here
    # For example, save the data as a JSON file
    with open("exchange_rates.json", "w") as file:
        json.dump(data, file)  # Saving the response data to a JSON file

else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


