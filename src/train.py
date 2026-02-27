import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


def train():
    df = pd.read_csv("/Users/samidhachari/Downloads/pythonML/Project/Context_Engine/scripts/driver_context_dataset.csv")

    # Create encoders
    location_encoder = LabelEncoder()
    traffic_encoder = LabelEncoder()
    time_encoder = LabelEncoder()
    target_encoder = LabelEncoder()

    # Encode features
    df["location_type"] = location_encoder.fit_transform(df["location_type"])
    df["traffic_level"] = traffic_encoder.fit_transform(df["traffic_level"])
    df["time_of_day"] = time_encoder.fit_transform(df["time_of_day"])
    df["risk_level"] = target_encoder.fit_transform(df["risk_level"])

    # Features
    X = df.drop("risk_level", axis=1)
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_train, y_train)

    # SAVE EVERYTHING
    joblib.dump(model, "risk_model.pkl")
    joblib.dump(location_encoder, "location_encoder.pkl")
    joblib.dump(traffic_encoder, "traffic_encoder.pkl")
    joblib.dump(time_encoder, "time_encoder.pkl")
    joblib.dump(target_encoder, "target_encoder.pkl")

    print("Model and encoders saved successfully!")


if __name__ == "__main__":
    train()