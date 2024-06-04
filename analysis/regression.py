import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BW = 0.3
BUILTTYPES = ["blok", "apartamentowiec", "kamienica", "pozostale"]
COLS = ['distance_to_center', 'density', None]

df = pd.read_csv("data.csv")

values = np.vstack([df['longitude'], df['latitude']])
kde = gaussian_kde(values, bw_method=BW)

df['density'] = df.apply(lambda row: kde([row['longitude'], row['latitude']])[0], axis=1)
df['density'] /= df['density'].max()


# city center coordinates
city_center = (51.107792, 17.038641)

# Haversine formula to calculate distance between two lat-lon points
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Converting degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c * 1000
    return distance

df['distance_to_center'] = df.apply(lambda row: haversine(city_center[0], city_center[1], row['latitude'], row['longitude']), axis=1)




for builttype in BUILTTYPES:

    for counters, col in enumerate(COLS):
        print(builttype, col)
        df_filtered = df[df['builttype'] == builttype]
        if col:
            X = df_filtered[['m', col]]
        else:
            X = df_filtered[['m']]
        y = df_filtered['price']


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

        model = LinearRegression()
        model.fit(X_train, y_train)


        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        if len(model.coef_) == 1:
            print(f'y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}')
        else:
            print(f'y = {model.coef_[0]:.2f}x + {model.coef_[1]:.2f}z + {model.intercept_:.2f}')


        # Print the results
        print(f"RMSE: {rmse}")
        print(f"R^2: {r2}")
        print()
    
