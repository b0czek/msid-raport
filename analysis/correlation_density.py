import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

BANDWIDTHS = [
    [0.1, 0.15], 
    [0.3, 0.5]
]
BUILTTYPES = ["blok", "apartamentowiec", "kamienica", "pozostale"]

df = pd.read_csv("data.csv")
# df = df[(df['builttype'] == "apartamentowiec")]

for i,y in enumerate(BANDWIDTHS):
    for j,bw in enumerate(y):
        values = np.vstack([df['longitude'], df['latitude']])
        kde = gaussian_kde(values, bw_method=bw)
        col_name = f'density-{bw}'


        df[col_name] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)
        max_density = df[col_name].max()
        df[col_name] /= max_density
        for builttype in BUILTTYPES:
            print(builttype)

            df_filtered = df[(df['builttype'] == builttype)]
            print(df_filtered[['price', 'm', col_name]].corr())
        print()