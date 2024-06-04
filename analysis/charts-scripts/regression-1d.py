import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from args import parse_arguments

args = parse_arguments(add_arguments= lambda parser: parser.add_argument("builttype", type=str, help="Builttype of model"))


df = pd.read_csv(args.filename)
df = df[df['builttype'] == args.builttype]

X = df[['m']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.rcParams['font.size'] = 16

plt.scatter(df['m'], y, color='blue', label='Faktyczna cena')

plt.plot(X_test, y_pred, color='red', label='Przewidywana cena mieszkania')

plt.title(f'Regresja liniowa - {args.builttype}')
plt.xlabel('Powierzchnia mieszkania [m²]')
plt.ylabel('Cena [PLN]')
plt.legend()
plt.grid(True)
plt.savefig(f"regression-{args.builttype}.png")