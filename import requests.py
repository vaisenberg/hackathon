                     
import requests
api_key = '8BE2DED12194464:5D264E3F628D440'
url = f'https://api.tradingeconomics.com/markets/forecasts/symbol/AAPL:US?c={api_key}'
data = requests.get(url).json()
print(data)

 

