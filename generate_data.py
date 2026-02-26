import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

cities = {
    "Mumbai": 18000,
    "Delhi": 15000,
    "Bengaluru": 12000,
    "Pune": 8000,
    "Hyderabad": 7000,
    "Chennai": 7500,
    "Kolkata": 6000,
    "Ahmedabad": 5500,
    "Jaipur": 5000,
    "Lucknow": 4500
}

growth_volatility = {
    "Mumbai": 1.10,
    "Delhi": 1.05,
    "Bengaluru": 1.08,
    "Pune": 1.04,
    "Hyderabad": 1.06,
    "Chennai": 1.03,
    "Kolkata": 1.02,
    "Ahmedabad": 1.02,
    "Jaipur": 1.01,
    "Lucknow": 1.01
}

location_multiplier = {
    "Premium": 1.3,
    "Standard": 1.0,
    "Developing": 0.85
}

furnishing_bonus = {
    "Furnished": 500000,
    "Semi-Furnished": 250000,
    "Unfurnished": 0
}

data = []

for _ in range(5000): 

    city = random.choice(list(cities.keys()))
    base_price = cities[city]

    # Skewed area distribution (normal distribution)
    area = int(np.random.normal(1200, 400))
    area = max(400, min(area, 3500))

    # Link BHK to area
    if area < 700:
        bhk = random.choice([1])
    elif area < 1200:
        bhk = random.choice([2])
    elif area < 2000:
        bhk = random.choice([2, 3])
    else:
        bhk = random.choice([3, 4, 5])

    bathrooms = min(bhk, random.randint(1, 4))
    parking = random.randint(0, 1)
    location = random.choice(list(location_multiplier.keys()))
    age = random.randint(0, 25)
    furnishing = random.choice(list(furnishing_bonus.keys()))

    base_property_price = (
        base_price * area *
        location_multiplier[location]
    )

    structural_adjustment = (
        bhk * 180000 +
        bathrooms * 90000 +
        parking * 120000 -
        age * 40000 +
        furnishing_bonus[furnishing]
    )

    # market noise ±8%
    noise = np.random.normal(1.0, 0.08)

    # city volatility factor
    volatility = growth_volatility[city]

    price = (base_property_price + structural_adjustment) * noise * volatility

    data.append([
        city, area, bhk, bathrooms,
        parking, location, age,
        furnishing, round(price, 0)
    ])

columns = [
    "city", "area_sqft", "bhk",
    "bathrooms", "parking",
    "location_type", "property_age",
    "furnishing", "price"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/housing_data.csv", index=False)

print("Refined dataset generated successfully!")