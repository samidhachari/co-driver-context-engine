import pandas as pd
import joblib
from sklearn.metrics import classification_report
from preprocess import preprocess_data


def evaluate():
    df = pd.read_csv("/Users/samidhachari/Downloads/pythonML/Project/Context_Engine/scripts/driver_context_dataset.csv")
    df, _, _ = preprocess_data(df)

    X = df.drop("risk_level", axis=1)
    y = df["risk_level"]

    model = joblib.load("/Users/samidhachari/Downloads/pythonML/Project/Context_Engine/src/risk_model.pkl")

    y_pred = model.predict(X)

    print(classification_report(y, y_pred))


if __name__ == "__main__":
    evaluate()