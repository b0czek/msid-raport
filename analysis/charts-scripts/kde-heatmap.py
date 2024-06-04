import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from args import parse_arguments

BANDWIDTHS = [
    [0.1, 0.15], 
    [0.3, 0.5]
]

args = parse_arguments()

df = pd.read_csv(args.filename)

plt.rcParams['font.size'] = 16
fig, axs = plt.subplots(2, 2, figsize=(16,10)) 



for i,y in enumerate(BANDWIDTHS):
    for j,bw in enumerate(y):
        values = np.vstack([df['longitude'], df['latitude']])
        kde = gaussian_kde(values, bw_method=bw)

        # Create grid for heatmap
        xmin, xmax = df['longitude'].min(), df['longitude'].max()
        ymin, ymax = df['latitude'].min(), df['latitude'].max()
        x, y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([x.ravel(), y.ravel()])
        density = kde(positions).reshape(x.shape)

        axs[i,j].imshow(np.rot90(density), cmap='viridis', extent=[xmin, xmax, ymin, ymax])


        axs[i,j].set_title(f'Gęstość ogłoszeń, h = {bw}')
        axs[i,j].set_xlabel('Długość geograficzna [°]')
        axs[i,j].set_ylabel('Szerokość geograficzna [°]')
        axs[i,j].grid(True)

plt.tight_layout()
plt.savefig("kde-heatmap.png")

