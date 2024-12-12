import logging
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class LaborCSV:
    Datum: pd.Series
    Startzeit: pd.Series
    Geschlecht: pd.Series
    Geburtsdatum: pd.Series
    Teilnehmer_ID: pd.Series
    Firma: pd.Series
    Frimen_ID: pd.Series


@dataclass
class AccountingXLSX:
    Datum: pd.Series
    Startzeit: pd.Series
    ID: pd.Series
    Anrede: pd.Series
    Nachname: pd.Series
    Vorname: pd.Series
    Geburtsdatum: pd.Series
    Adresse_original: pd.Series
    Adresse: pd.Series
    Postleitzahl: pd.Series
    Ort: pd.Series
    Email: pd.Series
    Telefonnummer: pd.Series
    Anwesenheit: pd.Series
    Kommentar: pd.Series


def parse_adress(x: str):
    m = re.match("(.*),\s?([0-9]{4,5})\s?(.*)", x)
    n = re.match("(.*)\s([0-9]{4,5})\s([a-zA-Z]+)", x)
    if m:
        return pd.Series(
            dict(
                adress=m.groups()[0].title(),
                postal_code=m.groups()[1],
                city=m.groups()[2].title(),
                original=x,
            )
        )
    elif n:
        return pd.Series(
            dict(
                adress=n.groups()[0].title(),
                postal_code=n.groups()[1],
                city=n.groups()[2].title(),
                original=x,
            )
        )
    else:
        logging.warning(f"Adress: '{x}' could not be parsed succesfully")
        return pd.Series(
            dict(
                adress="",
                postal_code="",
                city="",
                original=x,
            )
        )


def load_source(path: Path):
    suffix = path.suffix
    if suffix == ".xlsx":
        return pd.read_excel(path)
    elif suffix == ".tsv":
        return pd.read_csv(path, sep="\t")
    else:
        raise NotImplementedError(f"file of type {suffix} can not be processed.")


@dataclass
class OutputFileContainer:
    labor: pd.DataFrame
    accounting: pd.DataFrame
