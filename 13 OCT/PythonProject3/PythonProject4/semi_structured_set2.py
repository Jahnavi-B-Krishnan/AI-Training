import json
import pandas as pd

with open('smart_home_devices.json') as json_file:
   data = json.load(json_file)

# for i in data:
#     print(i["device_id"],i["device_type"],i["room"])

# for s in data:
#     if s["status"]=="Active":
#         print(s)

# for b in data:
#     if b["metrics"]["battery"] <60:
#         print(b)

# for d in data:
#     if "temperature" in d.get("metrics", {}):
#           print(d["device_id"], ":", d["metrics"]["temperature"])

# for d in data:
#     if "alerts" in d:
#         print(d)

# from collections import Counter
# print(Counter(dt["device_type"] for dt in data))

for h in data:
    if h['metrics']['battery'] >=70:
        h['health'] = 'good'
    elif 50 <= h['metrics']['battery'] <= 69 :
        h['health'] = 'moderate'
    elif h['metrics']['battery'] < 50:
        h['health'] = 'low'

with open('device_health_report.json', 'w') as outfile:
    json.dump(data, outfile)

df=pd.json_normalize(data)
# print(df[["device_id","device_type","room","status","metrics.battery","health"]])

print(df[(df['status']=="Active")&(df['metrics.battery']<70)])