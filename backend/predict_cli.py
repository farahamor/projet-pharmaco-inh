import sys
import json

from prediction import predict_dp_c2, calculate_doses


def main():

    try:
        # Lire les données envoyées par Electron
        data = json.loads(sys.stdin.read())

        dp_c1 = float(data["dp_c1"])
        gender = int(data["gender"])
        weight = float(data["weight"])

        # Prédiction ML
        y = predict_dp_c2(dp_c1, gender)

        # Calcul des doses
        doses = calculate_doses(y, weight)

        result = {
            "success": True,
            "dp_c2": float(y),
            "dose_min": float(doses["dose_min"]),
            "dose_average": float(doses["dose_average"]),
            "dose_max": float(doses["dose_max"])
        }

        print(json.dumps(result))

    except Exception as e:

        result = {
            "success": False,
            "error": str(e)
        }

        print(json.dumps(result))


if __name__ == "__main__":
    main()