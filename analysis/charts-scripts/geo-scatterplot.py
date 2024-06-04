import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from args import parse_arguments

args = parse_arguments(add_arguments = lambda parser: parser.add_argument('--price', action="store_true", help='Add scatter points color and size based on price'))


df = pd.read_csv(args.filename)



plt.figure(figsize=(10, 6))
plt.rcParams['font.size'] = 16

if args.price:
    sns.scatterplot(data=df, x='longitude', y='latitude', size='price', hue='price', palette="cool", sizes=(20, 200), legend=None)
else:
    sns.scatterplot(data=df, x='longitude', y='latitude', sizes=(20, 200), legend=None)

plt.title('Rozrzut położenia geograficznego mieszkań')
plt.xlabel('Długość geograficzna [°]')
plt.ylabel('Szerokość geograficzna [°]')
plt.grid(True)
plt.savefig("geo-scatterplot.png")
