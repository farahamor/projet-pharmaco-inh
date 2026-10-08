import sys
import json

from database import add_patient


def main():

    try:

        data = json.loads(sys.stdin.read())

        patient = {

            "Nom": data.get("nom", ""),
            "Prénom": data.get("prenom", ""),
            "Age (ans)": data.get("age"),
            "GENDER": data.get("gender"),
            "Poids (kg)": data.get("poids"),
            "Dose (mg/jour)": data.get("dose"),
            "C3 (mg/L)": data.get("c3"),

            "Dose pondérale (mg/kg/jour)":
                data.get("dp"),

            "DP/C1":
                data.get("dp") / data.get("c3"),

            "Y = DP/C2 prédit":
                data.get("dp_c2_pred"),

            "Dose min (mg/jour)":
                data.get("dose_min"),

            "Dose moyenne (mg/jour)":
                data.get("dose_average"),

            "Dose max (mg/jour)":
                data.get("dose_max"),

            "C2 réel (mg/L)": None,

            "DP/C2 réel": None,

            "Training": "NON",

            "Model_Version": "Linear Regression",

            "Date_Enregistrement": None,

            "Date_Training": None
        }


        new_id = add_patient(patient)


        print(json.dumps({

            "success": True,

            "id": new_id

        }))


    except Exception as e:

        print(json.dumps({

            "success": False,

            "error": str(e)

        }))


if __name__ == "__main__":

    main()