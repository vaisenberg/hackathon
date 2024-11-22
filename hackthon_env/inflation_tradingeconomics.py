import requests

# Your API key and URL (replace this with the correct URL and API key)
api_key = '8BE2DED12194464:5D264E3F628D440'
url = f'https://api.tradingeconomics.com/country/israel?c={api_key}'

# Send a GET request to fetch data from the Trading Economics API
response = requests.get(url)

# Check if the response was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    
    # Loop through each record and find the "Inflation Rate"
    for record in data:
        if record['Category'] == 'Inflation Rate':
            inflation_rate = record['LatestValue']
            print(f"Latest Inflation Rate: {inflation_rate}%")
else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")









