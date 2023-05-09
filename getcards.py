import pandas as pd
import re

# Function to convert the text to a dictionary
def get_cards(card_string):
    # Define regular expressions for each field
    name_pattern = r'^([^\[]+)' 
    type_pattern = r'\[(.*?)\]'
    number_pattern = r'#(\d+)'
    series_pattern = r'Pokemon (.+)'

    # Apply each pattern to the card string
    name_match = re.search(name_pattern, card_string)
    # Handles 2 types of names: 1) With the type, which is written within [ ] 2) Without the type, which is common, which does not contain the [ ]
    if name_match:
        name = name_match.group(1) # If there is [] in the name
    else:
        name_pattern = r'(.+?) #' # If the is no [] in the name
        name = re.search(name_pattern, card_string)
    number = re.search(number_pattern, card_string).group(1)
    card_type_match = re.search(type_pattern, card_string)
    # Handles if there is a type in the name otherwise the 'Type' is None
    if card_type_match:
        card_type = card_type_match.group(1)
    else:
        card_type = None
    series = re.search(series_pattern, card_string).group(1)

    # Create a dictionary and add the extracted values as key-value pairs
    card_data = {
        'Name': name,
        'Type': card_type,
        'Number': number,
        'Series': series
    }

    return(card_data)

url = 'https://www.pricecharting.com/offers?seller=7ugl5zx7u5td7l447wcxgbn6vy&status=collection' #Update the URL

# Read HTML table into a list of DataFrames
dfs = pd.read_html(url)

# Select the DataFrame which contains the Pokemon card data
df = dfs[1]['Item']

# Define the final DataFrame
card_list = pd.DataFrame(columns=['Name', 'Type', 'Number', 'Series', 'Grade'])

# Iterate through the items that contain the card data
for i in range(1,len(df),2):
    # Filters the items that are not a float item, this is because the 'float' items are 'nan' 
    if type(df[i]) != float:
        row = pd.Series(get_cards(df[i]))
        # Adds the series item as a new row to the final DataFrame
        row['Value'] = float(dfs[1]['Value'][i][1:5])
        row['Grade'] = (dfs[1]['Includes / Qty'][i])
        card_list = pd.concat([card_list, row.to_frame().T], ignore_index=True)

# Save the table to a file        
# card_list.to_json('card_list.json')
card_list.to_csv('card_list.csv')