import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from args import parse_arguments
from scipy.stats import gaussian_kde

BW = 0.3

BUILTTYPES = [
    ["blok", "apartamentowiec"],
    ["kamienica", "pozostale"]
]

args = parse_arguments()

df = pd.read_csv(args.filename)

plt.rcParams['font.size'] = 16
fig, axs = plt.subplots(2, 2, figsize=(16,10)) 


values = np.vstack([df['longitude'], df['latitude']])
kde = gaussian_kde(values, bw_method=BW)
df['density'] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)
max_density = df['density'].max()
df['density'] /= max_density



for i,y in enumerate(BUILTTYPES):
    for j,builttype in enumerate(y):
        print(builttype)
        filtered_df = df[df['builttype'] == builttype]
        # Calculate correlation
        correlation = np.corrcoef(filtered_df['density'], filtered_df['price'])[0, 1]
        print(f"Correlation coefficient between density and price: {correlation:.2f}")


        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(filtered_df['density'], filtered_df['price'])

        sns.regplot(x='density', y='price', data=filtered_df, scatter_kws={'color': 'blue', 's': 10},
                line_kws={'color': 'red', 'label': f'Linia regresji: y={slope:.2f}x+{intercept:.2f}\n$R^2$={(r_value ** 2):.2f}'}, ax=axs[i,j])

        # Plotting
        axs[i,j].set_title(f'Gęstość ofert vs Cena, {builttype}')
        axs[i,j].set_xlabel('Gęstość ofert')
        axs[i,j].set_ylabel('Cena [PLN]')
        axs[i,j].legend()
        axs[i,j].grid(True)

plt.tight_layout()
plt.savefig("density-price-builttype.png")