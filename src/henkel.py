import pandas as pd
from enum import Enum
import json


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
    
def normalize_henkel(df: pd.DataFrame) -> pd.DataFrame:
    firstnames_male, firstnames_female = load_male_and_female_names_list()

    name_first = df["Customer Name"].apply(
        lambda x: " ".join(x.strip().split(" ")[:-1]).title()
    )


    name_last = df["Customer Name"].apply(lambda x: x.strip().split(" ")[-1].title())

    gender = name_first.apply(lambda x: get_gender_by_firstname(x, firstnames_male=firstnames_male, firstnames_female=firstnames_female))


    data = {
        "Datum": df["Date Time"].dt.strftime('%d.%m.%Y'),
        "Startzeit": df["Date Time"].dt.time,
        "Geschlecht": gender,
        "Geburtsdatum": None, 
        "Teilnehmer-ID": None, 
        "Firma": None, 
        "Frimen-ID": None
    }

    df_labor = pd.DataFrame(data)
    return df_labor


def get_gender_by_firstname(
    firstname,
    firstnames_male, 
    firstnames_female
):
    if (firstname in firstnames_male) and (firstname not in firstnames_female):
        return Gender.MALE.value
    elif (firstname in firstnames_female) and (firstname not in firstnames_male):
        return Gender.FEMALE.value
    else:
        return Gender.NOT_DETERMINABLE.value
