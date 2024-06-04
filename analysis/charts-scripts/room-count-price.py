import pandas as pd
import matplotlib.pyplot as plt
from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)

rooms_price = df.groupby('rooms')['price'].mean()

plt.rcParams['font.size'] = 16
plt.figure(figsize=(10, 8))
rooms_price.plot(kind='bar')
plt.xlabel('Liczba pokojów')
plt.ylabel('Średnia cena [PLN]')
plt.title('Średnia cena vs liczba pokojów')
plt.savefig("room-count-price.png")
