import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)


fig, axs = plt.subplots(1, 2, figsize=(10,5)) 

sns.scatterplot(data=df, x='longitude', y='price', size='price', sizes=(20, 200), legend=None, ax=axs[0])
axs[0].set_title('Cena vs Długość geograficzna')
axs[0].set_xlabel('Długość geograficzna [°]')
axs[0].set_ylabel('Cena [PLN]')
axs[0].grid(True)

df_sorted = df.sort_values('longitude')
window_size = 200
df_sorted['longitude_mean'] = df_sorted['price'].rolling(window=window_size, center=True).mean()

sns.lineplot(data=df_sorted, x='longitude', y='longitude_mean', ax=axs[0], color='red', label="Średnia cena")


sns.scatterplot(data=df, x='latitude', y='price', size='price', sizes=(20, 200), legend=None, ax=axs[1])
axs[1].set_title('Cena vs Szerokość geograficzna')
axs[1].set_xlabel('Szerokość geograficzna [°]')
axs[1].set_ylabel('Cena [PLN]')
axs[1].grid(True)

df_sorted = df.sort_values('latitude')
window_size = 500
df_sorted['latitude_mean'] = df_sorted['price'].rolling(window=window_size, center=True).mean()

sns.lineplot(data=df_sorted, x='latitude', y='latitude_mean', ax=axs[1], color='red', label="Średnia cena")


plt.tight_layout()
plt.savefig("coordinates-price.png")
