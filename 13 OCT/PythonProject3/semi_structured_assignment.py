import json
import pandas as pd

with open('semi_structured_data.json') as json_file:
    data = json.load(json_file)

# for i in data:
#     print(i["incident_id"])

# for l in data:
#     print(l["location"]['city'])

# for s in data:
#     if s["severity"]=="High":
#         print(s)

# for c in data:
#     if c['category']=="Safety":
#         print(c)

# for a in data :
#     print(a.get('actions','No actions recorded'))

# from collections import Counter
# print(Counter(incident["severity"] for incident in data))

# for st in data:
#     st['status']='open'
#
# with open("updated_incidents.json", "w") as file:
#     json.dump(data, file, indent=4)

df=pd.json_normalize(data)
print(df[['incident_id','severity','category','location.city','location.site']])

