import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold

BW = 0.3
BUILTTYPES = ["blok", "apartamentowiec", "kamienica", "pozostale"]
COLS = ['distance_to_center', 'density', None]

df = pd.read_csv("data.csv")

values = np.vstack([df['longitude'], df['latitude']])
kde = gaussian_kde(values, bw_method=BW)

df['density'] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)

# Define the city center coordinates
city_center = (51.107792, 17.038641)

# Haversine formula to calculate distance between two lat-lon points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c * 1000  # Distance in meters
    return distance

df['distance_to_center'] = df.apply(lambda row: haversine(city_center[0], city_center[1], row['latitude'], row['longitude']), axis=1)


kf = KFold(n_splits=5, shuffle=True, random_state=1)  

for builttype in BUILTTYPES:
    for col in COLS:
        print(f'Built Type: {builttype}, Feature: {col}')
        df_filtered = df[df['builttype'] == builttype]
        if col:
            X = df_filtered[['m', col]]
        else:
            X = df_filtered[['m']]
        y = df_filtered['price']

        rmses = []
        r2s = []

        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)

            rmses.append(rmse)
            r2s.append(r2)

        avg_rmse = np.mean(rmses)
        avg_r2 = np.mean(r2s)

        print(f"Average RMSE: {avg_rmse}")
        print(f"Average R²: {avg_r2}")
        print()
