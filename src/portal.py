from dataclasses import asdict

import pandas as pd

from src.common import (
    AccountingXLSX,
    GenericInput,
    LaborCSV,
    OutputFileContainer,
    parse_adress,
)


class PortalInput(GenericInput):
    pass

    def __init__(
        self,
        df,
    ):
        expected_columns = [
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

        optional_columns = []

        super().__init__(df, expected_columns, optional_columns)

    def normalize_input(df: pd.DataFrame) -> OutputFileContainer:
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
                    Anrede=df["Geschlecht"].map({"male": "Herr", "female": "Frau"}),
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

        return OutputFileContainer(labor=df_labor, accounting=df_accounting)
