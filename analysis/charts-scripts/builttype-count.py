import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)
plt.rcParams['font.size'] = 16

plt.figure(figsize=(12, 10))

ax = sns.countplot(
    x="builttype",
    data=df,
)
ax.bar_label(ax.containers[0])  
ax.set_title("Liczba ogłoszeń w zależności od rodzaju zabudowy")
ax.set_xlabel("Rodzaj zabudowy")
ax.set_ylabel("Liczba ogłoszeń")

plt.grid(True)


plt.savefig("builttype-count.png")

