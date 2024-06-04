import pandas as pd

df = pd.read_csv("data.csv")

print(df[['price', 'm', 'rooms', 'floor_select', 'longitude', 'latitude', 'rent']].corr())