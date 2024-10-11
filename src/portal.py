import pandas as pd
from dataclasses import asdict
from src.common import LaborCSV, AccountingXLSX, parse_adress

expected_columns_portal = [
    "Datum",
    "Startzeit",
    "Vorname",
    "Nachname",
    "Geschlecht",
    "Geburtsdatum",
    "Adresse",
    "Email",
    "Telefonnummer",
    "Antwort optionale Fragen",
    "Teilnehmer-ID",
    "Firma",
    "Firmen-ID",
    "Abteilung",
    "Kalender-Name",
    "Service-Name",
]


def normalize_portal_df(df: pd.DataFrame):

    adresses = df["Adresse"].apply(parse_adress)

    df_labor = pd.DataFrame(
        asdict(
            LaborCSV(
                Datum=df["Datum"],
                Startzeit=df["Startzeit"],
                Geschlecht=df["Geschlecht"].map({"male": "M", "female": "W"}),
                Geburtsdatum=df["Geburtsdatum"],
                Teilnehmer_ID=df["Teilnehmer-ID"],
                Firma=df["Firma"],
                Frimen_ID=df["Firmen-ID"],
            )
        )
    )

    df_accounting = pd.DataFrame(
        asdict(
            AccountingXLSX(
                Datum=df["Datum"],
                Startzeit=df["Startzeit"],
                ID=df["Teilnehmer-ID"],
                Anrede=df["Geschlecht"].map({"male": "M", "female": "W"}),
                Nachname=df["Nachname"],
                Vorname=df["Vorname"],
                Geburtsdatum=df["Geburtsdatum"],
                Adresse_original=None,
                Adresse=adresses["adress"],
                Postleitzahl=adresses["postal_code"].astype(str),
                Ort=adresses["city"],
                Email=df["Email"],
                Telefonnummer=df["Telefonnummer"],
                Anwesenheit=None,
                Kommentar=None,
            )
        )
    )

    return df_labor, df_accounting
