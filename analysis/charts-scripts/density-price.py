import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
from scipy.stats import gaussian_kde
from args import parse_arguments

BW = 0.3
args = parse_arguments()

df = pd.read_csv(args.filename)

values = np.vstack([df['longitude'], df['latitude']])
kde = gaussian_kde(values, bw_method=BW)
df['density'] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)

max_density = df['density'].max()
df['density'] /= max_density

correlation = np.corrcoef(df['density'], df['price'])[0, 1]
print(f"Correlation coefficient between density and price: {correlation:.2f}")

slope, intercept, r_value, p_value, std_err = stats.linregress(df['density'], df['price'])

plt.figure(figsize=(10, 6))
plt.rcParams['font.size'] = 16


ax = sns.regplot(x='density', y='price', data=df, scatter_kws={'color': 'blue', 's': 10}, line_kws={'color': 'red', 'label': f'Linia regresji: y={slope:.2f}x+{intercept:.2f}\n$R^2$={(r_value ** 2):.2f}'})

plt.title('Gęstość ofert vs Cena')
plt.xlabel('Gęstość ofert')
plt.ylabel('Cena [PLN]')

plt.legend()

plt.grid(True)
plt.savefig("density-price.png")