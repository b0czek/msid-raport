import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)
plt.rcParams['font.size'] = 16

plt.figure(figsize=(10, 6))
ax = sns.barplot(
    x="builttype",
    y='price',
    data=df,
    errorbar='sd',
    err_kws={'linewidth': 2}
)
plt.bar_label(ax.containers[0])  
plt.title("Średnia cena vs rodzaj zabudowy")
plt.xlabel("Rodzaj zabudowy")
plt.ylabel("Średnia cena [PLN]")

plt.grid(True)


plt.savefig("builttype-price.png")

