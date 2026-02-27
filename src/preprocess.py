import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_data(data):
    df = data.copy()

    categorical_cols = ["location_type", "traffic_level", "time_of_day"]

    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    target_encoder = LabelEncoder()
    df["risk_level"] = target_encoder.fit_transform(df["risk_level"])

    return df, encoders, target_encoder


data = pd.read_csv("/Users/samidhachari/Downloads/pythonML/Project/Context_Engine/scripts/driver_context_dataset.csv")
preprocess_data(data)