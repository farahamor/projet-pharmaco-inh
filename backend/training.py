import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
        BASE_DIR
        / "data"
        / "INH_database_application.xlsx"
)

MODEL_PATH = (
        BASE_DIR
        / "models"
        / "model_INH.pkl"
)


def load_training_data():

    df = pd.read_excel(
        DATABASE_PATH,
        sheet_name="Patients"
    )

    # Variables nécessaires
    training = df[
        [
            "DP/C1",
            "GENDER",
            "DP/C2 réel"
        ]
    ].copy()

    # Supprimer les valeurs manquantes
    training = training.replace(
        [np.inf, -np.inf],
        np.nan
    )

    training = training.dropna()

    return training


def train_model():

    data = load_training_data()

    if len(data) < 10:
        raise ValueError(
            "Pas assez de données pour entraîner le modèle."
        )

    X = data[
        [
            "DP/C1",
            "GENDER"
        ]
    ]

    y = data["DP/C2 réel"]

    # Séparation pour évaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    # Modèle retenu lors de l'étape 2
    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    # Évaluation
    prediction = model.predict(X_test)

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            prediction
        )
    )

    mae = mean_absolute_error(
        y_test,
        prediction
    )

    r2 = r2_score(
        y_test,
        prediction
    )

    # Réentraînement final sur toutes les données
    model.fit(
        X,
        y
    )

    package = {

        "model": model,

        "features": [
            "DP/C1",
            "GENDER"
        ],

        "target": "DP/C2",

        "model_name": "Linear Regression",

        "n_training_observations": len(data),

        "metrics": {

            "RMSE": float(rmse),

            "MAE": float(mae),

            "R2": float(r2)
        }
    }

    joblib.dump(
        package,
        MODEL_PATH
    )

    return package


if __name__ == "__main__":

    package = train_model()

    print("===== MODÈLE INH =====")

    print(
        f"Modèle : {package['model_name']}"
    )

    print(
        f"N observations : "
        f"{package['n_training_observations']}"
    )

    print(
        f"RMSE : "
        f"{package['metrics']['RMSE']:.4f}"
    )

    print(
        f"MAE : "
        f"{package['metrics']['MAE']:.4f}"
    )

    print(
        f"R² : "
        f"{package['metrics']['R2']:.4f}"
    )

    print(
        f"Modèle sauvegardé : "
        f"{MODEL_PATH}"
    )