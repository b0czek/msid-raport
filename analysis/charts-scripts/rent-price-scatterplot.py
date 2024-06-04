import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)


fig, axs = plt.subplots(1, 2, figsize=(10,5)) 
plt.rcParams['font.size'] = 16

sns.scatterplot(data=df, x='rent', y='price', size='price', sizes=(20, 200), legend=None, ax=axs[0])
axs[0].set_title('Cena vs Czynsz')
axs[0].set_xlabel('Czynsz')
axs[0].grid(True)


sns.scatterplot(data=df, x='m', y='price', size='price', sizes=(20, 200), legend=None, ax=axs[1])
axs[1].set_title('Cena vs Powierzchnia')
axs[1].set_xlabel('Czynsz [PLN]')
axs[1].set_ylabel('Powierzchnia [m²]')

plt.tight_layout()
plt.savefig("rent-price-scatterplot.png")
