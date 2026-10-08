import joblib
from pathlib import Path


# Localisation du modèle
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model_INH.pkl"


def load_model():
    """
    Charge le modèle INH sauvegardé.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {MODEL_PATH}"
        )

    package = joblib.load(MODEL_PATH)

    return package


def predict_dp_c2(dp_c1, gender):
    """
    Prédit DP/C2 à partir de :
        - DP/C1
        - GENDER
    """

    package = load_model()

    model = package["model"]

    X = [[float(dp_c1), float(gender)]]

    prediction = model.predict(X)[0]

    return float(prediction)


def calculate_doses(y, weight):
    """
    Calcule les doses recommandées.
    """

    weight = float(weight)
    y = float(y)

    dose_min = y * weight
    dose_average = y * weight * 1.5
    dose_max = y * weight * 2

    return {
        "dose_min": dose_min,
        "dose_average": dose_average,
        "dose_max": dose_max
    }


def calculate_dp(dose, weight):
    """
    Calcule la dose pondérale.
    """

    dose = float(dose)
    weight = float(weight)

    if weight <= 0:
        raise ValueError("Le poids doit être supérieur à 0.")

    return dose / weight


def calculate_dp_c1(dp, c3):
    """
    C3 dans l'application = C1 du modèle.

    DP/C1 = DP/C3
    """

    dp = float(dp)
    c3 = float(c3)

    if c3 <= 0:
        raise ValueError(
            "La concentration C3 doit être supérieure à 0."
        )

    return dp / c3


if __name__ == "__main__":

    # Test simple
    weight = 60
    dose = 300
    c3 = 5
    gender = 1

    dp = calculate_dp(dose, weight)

    dp_c1 = calculate_dp_c1(dp, c3)

    y = predict_dp_c2(dp_c1, gender)

    doses = calculate_doses(y, weight)

    print("===== TEST INH =====")
    print(f"DP       : {dp:.4f}")
    print(f"DP/C1    : {dp_c1:.4f}")
    print(f"DP/C2    : {y:.4f}")
    print(f"Dose min : {doses['dose_min']:.2f} mg/j")
    print(f"Dose moy : {doses['dose_average']:.2f} mg/j")
    print(f"Dose max : {doses['dose_max']:.2f} mg/j")