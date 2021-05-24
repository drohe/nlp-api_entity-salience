import csv
import os
from google.cloud import language
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json

# reading the data from the file
with open('mreids.txt') as f: #this file is set up as a dictionary with the mreid as the key and the name of the entity as the value
    data = f.read()
d = json.loads(data)

posts = pd.read_csv("content.csv", encoding="iso-8859-1") #the first column includes a URL and the second contains the page's content.
posts_list = [posts.columns.values.tolist()] + posts.values.tolist()
client = language.LanguageServiceClient()


### START THE SET UP FOR YOUR OUTPUTS
projectOutput = input("Enter a name for this project folder: ") # YOU WILL BE PROMPTED IN THE COMMAND LINE TO NAME YOUR PROJECT
outputcsv = projectOutput +".csv" #the path for your CSV file
## Creating your CSV file
f = csv.writer(open(outputcsv, "w+", newline="\n", encoding="utf-8"))
entity_names = ["URL"]
[entity_names.append(x) for x in d.values()] # this creates a column for each
f.writerow(entity_names)
### END THE OUTPUTS SETUP

for post in posts_list:
    url = post[0];
    content = post[1];
    arr_salience = [url]
    if type(content) == str:
        doc = language.Document(content=content, type_=language.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=doc)
        entities = []
        [entities.append(x) for x in response.entities if x.name not in entities]
        for mid in d:
            salience = ''
            for entity in entities:
                entity_id = entity.metadata.get("mid","-")
                if entity_id == mid:
                    salience = "{:.1%}".format(entity.salience)
            arr_salience.append(salience)
    f.writerow(arr_salience)
