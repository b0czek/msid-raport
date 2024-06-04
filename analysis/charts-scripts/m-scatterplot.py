import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)

plt.figure(figsize=(10, 6))
plt.rcParams['font.size'] = 16
sns.scatterplot(data=df, x='m', y='price', size='price', sizes=(20, 200), legend=None)
plt.title('Cena vs Powierzchnia mieszkania')
plt.xlabel('Powierzchnia [m²]')
plt.ylabel('Cena [PLN]')
plt.grid(True)
plt.savefig("m-scatterplot.png")
