import pandas as pd
df= pd.read_csv('strustructured_data.csv')
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# print(df[['Shipment_ID','Origin','Destination','Cost']])

# print(df[df['Mode']=="Road"])

# print(df[df['Weight_Kg']>150])

# df['Cost_Per_Km']=df['Cost']/df['Distance_Km']
# # print(df)

# print("Average shipment cost:",(df['Cost'].mean()))
# print("Highest shipment cost:",(df['Cost'].max()))
# print("Lowest shipment cost:",(df['Cost'].min()))

# print(df.groupby('Mode')['Cost'].sum())

# print(df.groupby('Mode')['Weight_Kg'].mean())

# print(df.sort_values(by=['Cost'], ascending=False))

# print(df[(df['Delivery_Days']<=1)&(df['Cost']<5000)])


