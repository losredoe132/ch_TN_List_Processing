import json
import logging
from dataclasses import asdict
from enum import Enum

import pandas as pd

from src.common import AccountingXLSX, LaborCSV, parse_adress

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


def normalize_bookings_df(df: pd.DataFrame) -> pd.DataFrame:
    firstnames_male, firstnames_female = load_male_and_female_names_list()

    name_first = df["Customer Name"].apply(
        lambda x: " ".join(x.strip().split(" ")[:-1]).title()
    )

    name_last = df["Customer Name"].apply(lambda x: x.strip().split(" ")[-1].title())

    gender = name_first.apply(
        lambda x: get_gender_by_firstname(
            x, firstnames_male=firstnames_male, firstnames_female=firstnames_female
        )
    )

    adresses = df["Customer Address"].apply(parse_adress)

    df_labor = pd.DataFrame(
        asdict(
            LaborCSV(
                Datum=df["Date Time"].dt.strftime("%d.%m.%Y"),
                Startzeit=df["Date Time"].dt.time,
                Geschlecht=gender,
                Geburtsdatum=None,
                Teilnehmer_ID=None,
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
                ID=None,
                Anrede=gender.map({"M": "Herr", "W": "Frau"}),
                Nachname=name_last,
                Vorname=name_first,
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

    return df_labor, df_accounting


def get_gender_by_firstname(firstname, firstnames_male, firstnames_female):
    if (firstname in firstnames_male) and (firstname not in firstnames_female):
        logging.debug(f"Determine {firstname} as MALE")
        return Gender.MALE.value
    elif (firstname in firstnames_female) and (firstname not in firstnames_male):
        logging.debug(f"Determine {firstname} as FEMALE")
        return Gender.FEMALE.value
    else:
        logging.warning(f"Can not determine gender of {firstname}")
        return Gender.NOT_DETERMINABLE.value
