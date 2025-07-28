# Real Estate Bot for Dubai
# This script loads a sample real estate dataset and uses a simple linear regression
# implementation (gradient descent) to predict ROI for each property. It then prints
# the top 10 opportunities based on the predicted ROI.

import csv

DATA_FILE = 'dubai_real_estate.csv'
LEARNING_RATE = 0.01
EPOCHS = 1000
SIZE_SCALE = 6000.0  # max size in dataset
PRICE_SCALE = 12_000_000.0  # max price in dataset

# Encode categorical values to integers
def encode(values):
    mapping = {}
    encoded = []
    for v in values:
        if v not in mapping:
            mapping[v] = len(mapping)
        encoded.append(mapping[v])
    return encoded, mapping

# Load dataset
def load_dataset(path):
    data = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        locations = []
        types = []
        for row in reader:
            row['bedrooms'] = int(row['bedrooms'])
            row['size_sqft'] = float(row['size_sqft'])
            row['price'] = float(row['price'])
            row['rental_income'] = float(row['rental_income'])
            data.append(row)
            locations.append(row['location'])
            types.append(row['property_type'])
    loc_encoded, loc_map = encode(locations)
    type_encoded, type_map = encode(types)
    for i, row in enumerate(data):
        row['location_enc'] = loc_encoded[i]
        row['type_enc'] = type_encoded[i]
        row['roi'] = row['rental_income'] / row['price']
    return data, loc_map, type_map

# Prepare features and targets
def prepare_xy(data):
    X = []
    y = []
    for row in data:
        size = row['size_sqft'] / SIZE_SCALE
        price = row['price'] / PRICE_SCALE
        loc = row['location_enc'] / 10.0
        typ = row['type_enc'] / 10.0
        features = [1.0, row['bedrooms'], size, price, loc, typ]
        X.append(features)
        y.append(row['roi'])
    return X, y

# Gradient descent for linear regression
def train_linear_regression(X, y, epochs=EPOCHS, lr=LEARNING_RATE):
    n_features = len(X[0])
    weights = [0.0] * n_features
    for _ in range(epochs):
        for features, target in zip(X, y):
            pred = sum(w * f for w, f in zip(weights, features))
            error = pred - target
            for i in range(n_features):
                weights[i] -= lr * error * features[i]
    return weights

# Predict using the trained model
def predict(weights, features):
    return sum(w * f for w, f in zip(weights, features))

# Main logic
def main():
    data, loc_map, type_map = load_dataset(DATA_FILE)
    X, y = prepare_xy(data)
    weights = train_linear_regression(X, y)
    for i, row in enumerate(data):
        size = row['size_sqft'] / SIZE_SCALE
        price = row['price'] / PRICE_SCALE
        loc = row['location_enc'] / 10.0
        typ = row['type_enc'] / 10.0
        features = [1.0, row['bedrooms'], size, price, loc, typ]
        row['predicted_roi'] = predict(weights, features)
    data.sort(key=lambda r: r['predicted_roi'], reverse=True)
    print('Top 10 Investment Opportunities (predicted ROI):')
    for row in data[:10]:
        print(f"{row['property_id']} - Location: {row['location']} - Price: {row['price']} - "
              f"Rental: {row['rental_income']} - Predicted ROI: {row['predicted_roi']:.4f}")

if __name__ == '__main__':
    main()
