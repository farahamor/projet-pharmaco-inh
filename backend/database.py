import pandas as pd
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
        BASE_DIR
        / "data"
        / "INH_database_application.xlsx"
)


def load_database():
    """
    Charge la base Excel.
    """

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Base INH introuvable : {DATABASE_PATH}"
        )

    return pd.read_excel(
        DATABASE_PATH,
        sheet_name="Patients"
    )


def save_database(df):
    """
    Sauvegarde la base Excel.
    """

    structure_path = DATABASE_PATH

    # Lire la feuille Structure si elle existe
    try:
        structure = pd.read_excel(
            DATABASE_PATH,
            sheet_name="Structure"
        )
    except Exception:
        structure = None

    with pd.ExcelWriter(
            DATABASE_PATH,
            engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Patients",
            index=False
        )

        if structure is not None:
            structure.to_excel(
                writer,
                sheet_name="Structure",
                index=False
            )


def get_next_id(df):
    """
    Génère automatiquement le prochain ID.
    """

    if df.empty:
        return 1

    ids = pd.to_numeric(
        df["ID"],
        errors="coerce"
    )

    if ids.dropna().empty:
        return 1

    return int(ids.max()) + 1


def add_patient(patient_data):
    """
    Ajoute un nouveau patient dans la base.
    """

    df = load_database()

    patient_id = get_next_id(df)

    patient_data["ID"] = patient_id

    patient_data["Date_Enregistrement"] = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    new_patient = pd.DataFrame(
        [patient_data]
    )

    df = pd.concat(
        [df, new_patient],
        ignore_index=True
    )

    save_database(df)

    return patient_id


def update_patient(patient_id, updates):
    """
    Met à jour un patient existant.
    """

    df = load_database()

    mask = df["ID"] == patient_id

    if not mask.any():
        raise ValueError(
            f"Patient {patient_id} introuvable."
        )

    for column, value in updates.items():
        if column in df.columns:
            df.loc[mask, column] = value

    save_database(df)


if __name__ == "__main__":

    df = load_database()

    print("Base INH chargée.")
    print(f"Nombre d'observations : {len(df)}")
    print(df.head())