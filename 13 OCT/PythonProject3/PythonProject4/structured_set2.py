import pandas as pd

df=pd.read_csv('renewable_energy.csv')
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# print(df[df['Energy_Type'].isin(['Solar','Wind'])])

df['Efficiency_Percent'] = (df['Actual_Output_MW'] / df['Capacity_MW']) *100
# print(df)

# print(df[df['Efficiency_Percent']>85])

# print(df.groupby('Energy_Type')['Efficiency_Percent'].mean())

# print(df.groupby('Energy_Type')['Maintenance_Cost'].sum())

# print(df.loc[df['Actual_Output_MW'].idxmax()])

df['Cost_Per_MW']=df['Maintenance_Cost']/df['Actual_Output_MW']

# print(df.sort_values(by=['Cost_Per_MW'], ascending=True))

# print(df[(df['Efficiency_Percent']>80) & (df['Maintenance_Cost']<70000)])

import matplotlib.pyplot as plt

plt.bar(df['Plant_Name'],df['Efficiency_Percent'])
plt.xlabel("Plant_Name")
plt.ylabel("Efficiency (%)")
plt.show()