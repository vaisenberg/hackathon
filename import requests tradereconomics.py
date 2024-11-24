import requests

# Correct raw URL of the .whl file
url = "https://github.com/tradingeconomics/tradingeconomics/raw/master/python/dist/tradingeconomics-3.7-py3-none-any.whl"

# Send GET request to download the file
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    # Save the content to a file on your local machine
    with open("tradingeconomics-3.7-py3-none-any.whl", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download the file.")
