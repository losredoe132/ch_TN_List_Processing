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

    def normalize_input(self) -> OutputFileContainer:
        adresses = self.df["Adresse"].apply(parse_adress)

        df_labor = pd.DataFrame(
            asdict(
                LaborCSV(
                    Datum=self.df["Datum"],
                    Startzeit=self.df["Startzeit"],
                    Geschlecht=self.df["Geschlecht"].map({"male": "M", "female": "W"}),
                    Geburtsdatum=self.df["Geburtsdatum"],
                    Teilnehmer_ID=self.df["Teilnehmer-ID"],
                    Firma=self.df["Firma"],
                    Frimen_ID=self.df["Firmen-ID"],
                )
            )
        )

        df_accounting = pd.DataFrame(
            asdict(
                AccountingXLSX(
                    Datum=self.df["Datum"],
                    Startzeit=self.df["Startzeit"],
                    ID=self.df["Teilnehmer-ID"],
                    Anrede=self.df["Geschlecht"].map(
                        {"male": "Herr", "female": "Frau"}
                    ),
                    Nachname=self.df["Nachname"],
                    Vorname=self.df["Vorname"],
                    Geburtsdatum=self.df["Geburtsdatum"],
                    Adresse_original=None,
                    Adresse=adresses["adress"],
                    Postleitzahl=adresses["postal_code"].astype(str),
                    Ort=adresses["city"],
                    Email=self.df["Email"],
                    Telefonnummer=self.df["Telefonnummer"],
                    Anwesenheit=None,
                    Kommentar=None,
                )
            )
        )

        return OutputFileContainer(labor=df_labor, accounting=df_accounting)
