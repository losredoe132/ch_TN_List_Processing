import json
import logging
from dataclasses import asdict
from enum import Enum

import pandas as pd

from src.common import AccountingXLSX, LaborCSV, OutputFileContainer, parse_adress

expected_colums_bookings = [
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


class Gender(Enum):
    MALE = "M"
    FEMALE = "W"
    NOT_DETERMINABLE = " "


def load_male_and_female_names_list():
    with open("data/male.json", "r") as fh:
        firstnames_male = json.load(fh)

    with open("data/female.json", "r") as fh:
        firstnames_female = json.load(fh)

    return firstnames_male, firstnames_female


def normalize_bookings_df(df: pd.DataFrame) -> OutputFileContainer:
    firstnames_male, firstnames_female = load_male_and_female_names_list()

    df["Date Time"] = pd.to_datetime(df["Date Time"])

    df["Vorname"] = df["Customer Name"].apply(
        lambda x: " ".join(x.strip().split(" ")[:-1]).title()
    )

    df["Nachname"] = df["Customer Name"].apply(
        lambda x: x.strip().split(" ")[-1].title()
    )

    df["teilnehmerid"] = df.apply(
        lambda row: get_teilnehmerid(
            row,
        ),
        axis=1,
    )

    df["gender"] = df.apply(
        lambda x: get_gender_by_firstname(
            x, firstnames_male=firstnames_male, firstnames_female=firstnames_female
        ),
        axis=1,
    )

    adresses = df["Customer Address"].astype(str).apply(parse_adress)

    df_labor = pd.DataFrame(
        asdict(
            LaborCSV(
                Datum=df["Date Time"].dt.strftime("%d.%m.%Y"),
                Startzeit=df["Date Time"].dt.time,
                Geschlecht=df["gender"],
                Geburtsdatum=None,
                Teilnehmer_ID=df["teilnehmerid"],
                Firma=None,
                Frimen_ID=None,
            )
        )
    )

    df_accounting = pd.DataFrame(
        asdict(
            AccountingXLSX(
                Datum=df["Date Time"].dt.strftime("%d.%m.%Y"),
                Startzeit=df["Date Time"].dt.time,
                ID=df["teilnehmerid"],
                Anrede=df["gender"].map({"M": "Herr", "W": "Frau"}),
                Nachname=df["Nachname"],
                Vorname=df["Vorname"],
                Geburtsdatum=None,
                Adresse_original=adresses["original"],
                Adresse=adresses["adress"],
                Postleitzahl=adresses["postal_code"].astype(str),
                Ort=adresses["city"],
                Email=df["Customer Email"],
                Telefonnummer=df["Customer Phone"].astype(str),
                Anwesenheit=None,
                Kommentar=None,
            )
        )
    )

    return OutputFileContainer(labor=df_labor, accounting=df_accounting)


def get_gender_by_firstname(row, firstnames_male, firstnames_female):
    input_msg = "  Please type:\n  M/m for male\n  F/w for female."
    firstname = row["Vorname"]

    if (firstname in firstnames_male) and (firstname not in firstnames_female):
        logging.debug(f"Determine {firstname} as MALE")
        return Gender.MALE.value
    elif (firstname in firstnames_female) and (firstname not in firstnames_male):
        logging.debug(f"Determine {firstname} as FEMALE")
        return Gender.FEMALE.value
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


def get_teilnehmerid(row: pd.Series):
    print("-" * 100)
    print(row[["Vorname", "Nachname", "Customer Email", "Customer Address"]])
    # validate
    try_count = 0
    while try_count < 3:
        i = input("Please insert the TeilnehmerID and press enter:\n")

        if len(str(i)) == 6 and (i.isnumeric()):
            return i
        print(f"Invalid TeilnehmerID {i}. Has to be 6 numeric chars. Try again...")
