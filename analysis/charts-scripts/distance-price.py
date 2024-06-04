import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from args import parse_arguments

args = parse_arguments()


df = pd.read_csv(args.filename)

# Define the city center coordinates
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

correlation = np.corrcoef(df['distance_to_center'], df['price'])[0, 1]
print(f"Correlation coefficient between distance and price: {correlation:.2f}")

slope, intercept, r_value, p_value, std_err = stats.linregress(df['distance_to_center'], df['price'])

plt.figure(figsize=(10, 6))
plt.scatter(df['distance_to_center'], df['price'], color='blue', label='Data Points')
plt.plot(df['distance_to_center'], intercept + slope * df['distance_to_center'], 'r', label=f'Linia regresji: y={slope:.2f}x+{intercept:.2f}\n$R^2$={(r_value ** 2):.2f}')
plt.title('Odległość od centrum vs Cena')
plt.xlabel('Odległość od centrum [metry]')
plt.ylabel('Cena [PLN]')
plt.rcParams['font.size'] = 16
plt.legend()
plt.grid(True)
plt.savefig("distance-price.png")