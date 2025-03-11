import json
import logging
from dataclasses import asdict

import pandas as pd

from src.common import (
    AccountingXLSX,
    Gender,
    GenericInput,
    LaborCSV,
    OutputFileContainer,
)

logger = logging.getLogger(__name__)


class BookingsInput(GenericInput):
    def __init__(self, df):
        expected_columns = [
            "Date Time",
            "Customer Name",
            "Customer Email",
            "Customer Phone",
            "Customer Address",
            "Staff",
            "Staff Name",
            "Staff Email",
            "Service",
            "Location",
            "Duration (mins.)",
            "Pricing Type",
            "Price",
            "Currency",
            "Cc Attendees",
            "Signed Up Attendees Count",
            "Text Notifications Enabled",
            " Custom Fields",
            "Event Type",
            "Booking Id",
            "Tracking Data",
        ]

        optional_columns = [
            "ID",
            "Geburtsdatum",
        ]

        super().__init__(df, expected_columns, optional_columns)

    def parse_booking_adress(self, x):
        j = json.loads(x)

        return pd.Series(
            dict(
                adress=j["Straße & Hausnummer (Rechnungsadresse)"],
                postal_code=j["PLZ (Rechnungsadresse)"],
                city=j["Ort (Rechnungsadresse)"],
            )
        )

    def parse_booking_date_of_birth(self, x):
        j = json.loads(x)

        return j["Geburtsdatum"]

    def normalize_input(self) -> OutputFileContainer:
        firstnames_male, firstnames_female = self.load_male_and_female_names_list()

        self.df["Date Time"] = pd.to_datetime(self.df["Date Time"])

        self.df["Vorname"] = self.df["Customer Name"].apply(
            lambda x: " ".join(x.strip().split(" ")[:-1]).title()
        )

        self.df["Nachname"] = self.df["Customer Name"].apply(
            lambda x: x.strip().split(" ")[-1].title()
        )

        self.df["gender"] = self.df.apply(
            lambda x: self.get_gender_by_firstname(
                x, firstnames_male=firstnames_male, firstnames_female=firstnames_female
            ),
            axis=1,
        )

        adresses = (
            self.df[" Custom Fields"].astype(str).apply(self.parse_booking_adress)
        )

        date_of_births = (
            self.df[" Custom Fields"]
            .astype(str)
            .apply(self.parse_booking_date_of_birth)
        )

        self.handle_optional_columns()

        df_labor = pd.DataFrame(
            asdict(
                LaborCSV(
                    Datum=self.df["Date Time"].dt.strftime("%d.%m.%Y"),
                    Startzeit=self.df["Date Time"].dt.time,
                    Geschlecht=self.df["gender"],
                    Geburtsdatum=date_of_births,
                    Teilnehmer_ID=self.df["ID"],
                    Firma=None,
                    Frimen_ID=None,
                )
            )
        )

        df_accounting = pd.DataFrame(
            asdict(
                AccountingXLSX(
                    Datum=self.df["Date Time"].dt.strftime("%d.%m.%Y"),
                    Startzeit=self.df["Date Time"].dt.time,
                    ID=self.df["ID"],
                    Anrede=self.df["gender"].map({"M": "Herr", "W": "Frau"}),
                    Nachname=self.df["Nachname"],
                    Vorname=self.df["Vorname"],
                    Geburtsdatum=date_of_births,
                    Adresse=adresses["adress"],
                    Postleitzahl=adresses["postal_code"].astype(str),
                    Ort=adresses["city"],
                    Email=self.df["Customer Email"],
                    Telefonnummer=self.df["Customer Phone"].astype(str),
                    Anwesenheit=None,
                    Kommentar=None,
                )
            )
        )

        return OutputFileContainer(labor=df_labor, accounting=df_accounting)

    def load_male_and_female_names_list(self):
        with open("data/male.json", "r") as fh:
            firstnames_male = json.load(fh)

        with open("data/female.json", "r") as fh:
            firstnames_female = json.load(fh)

        return firstnames_male, firstnames_female

    def get_gender_by_firstname(self, row, firstnames_male, firstnames_female):
        input_msg = "  Please type:\n  M/m for male\n  F/w for female."
        firstname = row["Vorname"]
        lastname = row["Nachname"]

        if (firstname in firstnames_male) and (firstname not in firstnames_female):
            logging.debug(f"Determine {firstname} as MALE")
            return Gender.MALE.value
        elif (firstname in firstnames_female) and (firstname not in firstnames_male):
            logging.debug(f"Determine {firstname} as FEMALE")
            return Gender.FEMALE.value
        elif (firstname == "") and (lastname in ["Block", "Blocker"]):
            logging.warning(
                f"Determine firstname: {firstname} lastname: {lastname} as MALE"
            )
            return Gender.MALE.value
        else:
            logging.warning(
                f"Can not determine gender of:\n{row['Vorname']}\n{row['Nachname']}\n{row['Customer Email']}"
            )
            i = input(input_msg).lower()
            try_count = 0
            while try_count < 3:
                if i in ["m"]:
                    return Gender.MALE.value
                elif i in ["w", "f"]:
                    return Gender.FEMALE.value
                else:
                    print("invalid input. try again...")
                    i = input(input_msg).lower()

            raise ValueError("retries exceeded.")
