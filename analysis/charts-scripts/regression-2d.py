import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy.stats import gaussian_kde
from mpl_toolkits.mplot3d import Axes3D

from args import parse_arguments

args = parse_arguments(add_arguments= lambda parser: parser.add_argument("builttype", type=str, help="Builttype of model"))


df = pd.read_csv(args.filename)
df = df[df['builttype'] == args.builttype]



values = np.vstack([df['longitude'], df['latitude']])
kde = gaussian_kde(values, bw_method=0.3)
df['density'] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)
df['density'] /= df['density'].max()




X = df[['m', 'density']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)






fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X_test['m'], X_test['density'], y_test, color='blue', label='Faktyczna cena')

m_range = np.linspace(X_test['m'].min(), X_test['m'].max(), 20)
density_range = np.linspace(X_test['density'].min(), X_test['density'].max(), 20)
m_grid, density_grid = np.meshgrid(m_range, density_range)
X_grid = np.c_[m_grid.ravel(), density_grid.ravel()]

y_grid_pred = model.predict(X_grid).reshape(m_grid.shape)
ax.plot_surface(m_grid, density_grid, y_grid_pred, color='red', alpha=0.5, label='Płaszczyzna regresji')

# Labels and title
ax.set_title(f'Regresja liniowa z dwoma zmiennymi wolnymi - {args.builttype}')
ax.set_xlabel('Powierzchnia [m²]')
ax.set_ylabel('Gęstość')
ax.set_zlabel('Cena [PLN]')

plt.legend()
plt.savefig(f"regression-2d-{args.builttype}.png")