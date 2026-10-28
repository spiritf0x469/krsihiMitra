
import os
import sys
import pickle
import subprocess
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "crop_yield.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
TRAIN_PATH = os.path.join(BASE_DIR, "train.py")

df = pd.read_csv(DATA_PATH)

df["Season"] = df["Season"].str.strip().str.lower()
df["State"] = df["State"].str.strip().str.lower()
df["Crop"] = df["Crop"].str.strip()

# Train the model if it does not exist.
if not os.path.exists(MODEL_PATH):
    print("Model not found. Training the model...")
    subprocess.run(
        [sys.executable, TRAIN_PATH],
        cwd=BASE_DIR,
        check=True
    )

# Load the trained model.
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


def recommend_crops(state, season, area, rainfall, top_n=3):
    state = state.strip().lower()
    season = season.strip().lower()

    data = df[
        (df["State"] == state) &
        (df["Season"] == season)
    ]

    if data.empty:
        return []

    crops = data["Crop"].unique()
    predictions = []
    latest_year = int(df["Crop_Year"].max())

    for crop in crops:
        crop_data = data[data["Crop"] == crop]

        avg_fert = crop_data["Fertilizer"].mean()
        avg_pest = crop_data["Pesticide"].mean()

        input_data = pd.DataFrame([{
            "Crop": crop,
            "Crop_Year": latest_year,
            "Season": season,
            "State": state,
            "Area": area,
            "Annual_Rainfall": rainfall,
            "Fertilizer": avg_fert,
            "Pesticide": avg_pest
        }])

        predicted_yield = model.predict(input_data)[0]

        predictions.append({
            "Crop": crop,
            "predicted_yield": round(float(predicted_yield), 2)
        })

    predictions.sort(
        key=lambda x: x["predicted_yield"],
        reverse=True
    )

    recommendations = predictions[:top_n]

    for rank, recommendation in enumerate(recommendations, start=1):
        recommendation["rank"] = rank

    return recommendations


def get_options():
    combinations = (
        df[["State", "Season"]]
        .drop_duplicates()
        .sort_values(["State", "Season"])
    )

    options = {}

    for _, row in combinations.iterrows():
        state = row["State"]
        season = row["Season"]

        if state not in options:
            options[state] = []

        options[state].append(season)

    return options
