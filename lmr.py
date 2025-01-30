#   checking to see if pushing to github is working  

#   The purpose of this code is to pull the data from the forms created in Kobotool box
#   and then use it to create things like a csv file or turn it into a pandas data frame that 
#   that can be used to product graphs 


import os
import pandas as pd
import requests
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

BASE_URL = "https://eu.kobotoolbox.org/api/v2"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# read in secrets.yaml
with open("secrets.yml") as file:
    secrets = yaml.safe_load(file)
token = secrets["personal_api_token"]
form_id = "a8uCNcYY8At6dDfkqP88oW"  # in the URL in a browser

headers = {"Authorization": f"Token {token}"}
data_url = f"{BASE_URL}/assets/{form_id}/data.json"
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    bird_df = pd.DataFrame(data["results"])
else:
    print(f"Failed to fetch data from form {form_id}, check the form id and token.")

#   dropping the columns that the form has created that I will not be using in the graphs
bird_df = bird_df.drop(columns=['_id', 'formhub/uuid','start', 'end','_xform_id_string', '_uuid','_attachments', '_status','_geolocation', '_submission_time','_tags', '_notes','__version__','meta/instanceID','_validation_status','_submitted_by'])
bird_df = bird_df.drop(columns=['table/Total_Owls','table/Total_Parrots','table/Total_Penguins','table/Total_Toucans','table/Total_Chickens','table/Total_Cranes','table/Overall_Totals','table/Male_Totals','table/Female_Totals'])

#   Renaming the columns so they are more usable
bird_df = bird_df.rename(columns={'table/Total_Owls':'Total Owls','table/Total_Parrots':'Total Parrots','table/Total_Penguins':'Total Penguins','table/Total_Toucans':'Total Toucans','table/Total_Chickens':'Total Chickens','table/Total_Cranes':'Total Cranes'})
bird_df = bird_df.rename(columns={'table/Female_Owls':'Female Owls','table/Female_Parrots':'Female Parrots','table/Female_Penguins':'Female Penguins','table/Female_Toucans':'Female Toucans','table/Female_Chickens':'Female Chickens','table/Female_Cranes':'Female Cranes'})
bird_df = bird_df.rename(columns={'table/Male_Owls':'Male Owls','table/Male_Parrots':'Male Parrots','table/Male_Penguins':'Male Penguins','table/Male_Toucans':'Male Toucans','table/Male_Chickens':'Male Chickens','table/Male_Cranes':'Male Cranes'})
bird_df = bird_df.rename(columns={'table/Male_Totals':'Male Totals','table/Female_Totals':'Female Totals','table/Overall_Totals':'Overall Totals'})

#   Here I have used the .melt() method to turn each one of the column titles into
#   a value in the column I named "Bird_Gender" next I have turn the values for each
#   of these into another column called "Count".
#   These two together have formed a new dataframe called bird_melted which is closer 
#   to the format that I need to use the .lmplot() method
bird_melted = bird_df.melt(var_name='Bird_Gender', value_name='Count')

#   This next piece of code is used to create a new column called "Gender" this is done by 
#   using a lambda function that will interate tho the Bird_Gender column and if it 
#   contains the String "Male" it will add the new value "Male" to a new column "'Gender' if
#   it doesnt then it will add the value "Female"
bird_melted['Gender'] = bird_melted['Bird_Gender'].apply(lambda x: 'Male' if 'Male' in x else 'Female')
#   This next will create a new column that will record the type of bird  in a new column named "type of bird"
#   it does this using a .str.replace() method to replace the redundant parts of "Bird_Gender" 
bird_melted['Type of Bird'] = bird_melted['Bird_Gender'].str.replace('Male ', '').str.replace('Female ', '')
#   next we get ride of the "Bird_Gender" column as this is now redundant 
bird_melted = bird_melted.drop(columns=['Bird_Gender'])

#   I have changed this variable so I dont have to type as much
bdf = bird_melted

#   Initialize an empty list for the transformed rows
transformed_rows = []

#   Iterate through the unique bird types
for bird_type in bdf['Type of Bird'].unique():
    #   Filter rows for the current bird type
    bird_rows = bdf[bdf['Type of Bird'] == bird_type]
    
    #   Separate male and female rows and convert to lists of dictionaries
    male_rows = bird_rows[bird_rows['Gender'] == 'Male'].to_dict('records')
    female_rows = bird_rows[bird_rows['Gender'] == 'Female'].to_dict('records')
    
    #   Create matches until one of the lists is exhausted
    while male_rows and female_rows:
        #   Pop the first male and female rows
        male_row = male_rows.pop(0)
        female_row = female_rows.pop(0)
        
        #   Append the match to the transformed rows
        transformed_rows.append({
            'Male': male_row['Count'],
            'Female': female_row['Count'],
            'Type of Bird': bird_type
        })

#   Create a new DataFrame from the transformed rows
result = pd.DataFrame(transformed_rows)

#   This is to make sure the data type is correct and can be used to make a chart
result['Male'] = pd.to_numeric(result['Male'], errors='coerce')
result['Female'] = pd.to_numeric(result['Female'], errors='coerce')


#   This creates a time stamp that shows when the file was made
current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
#   This will plot the lmplot chart 

sns.set_theme()
g = sns.lmplot(
    data = result,
    x="Male", y="Female", hue="Type of Bird",
    height=5,
    palette = "colorblind",
    markers=["o", "s", "D","v","x","+"]
)
plt.savefig(f"{OUTPUT_DIR}/birdlmr{current_date}.png")# This OUTPUT_DIR was made for use with .gitingore 


#   This saves the dataframe as a csv file 
bird_df.to_csv(f"{OUTPUT_DIR}/bird_data{current_date}.csv", index=False)