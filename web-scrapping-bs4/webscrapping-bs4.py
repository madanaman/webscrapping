import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL to checkout
static_url = "https://en.wikipedia.org/wiki/Tesla,_Inc.#cite_note-Tesla3Q2019-145"

#Fetch URL content
downloaded_html = requests.get(static_url)

#Parse html content
soup = BeautifulSoup(downloaded_html.text)

#Saving data to downloads directory
with open("downloads/downloaded_html_bs4.html", "w") as file:
    file.write(soup.prettify())

#Get Table content from the webpage
full_table = soup.select('table.wikitable tbody')[0]
# print(full_table)

#Prepare to extract column names
table_head = full_table.select('tr th')
table_columns = []
# print(table_head)
regex = re.compile('_\[\w\]')

for element in table_head:
    column_label = element.get_text(separator=" ", strip=True).replace(" ", "_")
    column_label = regex.sub("", column_label)
    table_columns.append(column_label)

#Prepare to extract column data
table_rows = full_table.select('tr')

table_data = []

for index, element in enumerate(table_rows):
    if index > 0:
        row_list =[]
        values = element.select('td')
        for value in values:
            enriched_value = value.get_text(separator=" ", strip=True)
            enriched_value = enriched_value.replace("+", "").replace(",", "").replace("[", "").replace("]", "").replace("~","")
            row_list.append(enriched_value)
        table_data.append(row_list)

# print(table_data)
#Push data to pandas dataframe for analysis
df = pd.DataFrame(table_data, columns=table_columns)
print(df)
