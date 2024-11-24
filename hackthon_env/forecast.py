import pandas as pd
import json

# Load your data (adjust path to your file)
df = pd.read_csv(r'C:\Users\vaise\OneDrive\Desktop\Hackthon_Project\hackthon_env\_markets_forecasts_currency.csv')

# Retrieve all data for rows where 'Symbol' is 'USDILS:CUR'
specific_row_and_columns = df.loc[df['Symbol'] == 'USDILS:CUR']

# Convert the DataFrame to a dictionary (by default, this will be a list of dictionaries, one for each row)
data_dict = specific_row_and_columns.to_dict(orient='records')

# Dump the dictionary into a JSON file
json_file_path = r'C:\Users\vaise\OneDrive\Desktop\Hackthon_Project\forecast_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

# Print the dictionary (to verify the result)
print(f"Data has been saved to {json_file_path}")

# To access the value of 'Forecast1' for each row:
for row in data_dict:
    forecast1_value = row.get('Forecast1')  # Retrieve the value for 'Forecast1'
    print(f"Forecast1 value: {forecast1_value}")
    forecast2_value = row.get('Forecast2')  # Retrieve the value for 'Forecast1'
    print(f"Forecast1 value: {forecast2_value}")
    forecast3_value = row.get('Forecast3')  # Retrieve the value for 'Forecast1'
    print(f"Forecast1 value: {forecast3_value}")
    forecast4_value = row.get('Forecast4')  # Retrieve the value for 'Forecast1'
    print(f"Forecast1 value: {forecast4_value}")





