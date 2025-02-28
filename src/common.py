import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pandas as pd
from typing import List


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


class Gender(Enum):
    MALE = "M"
    FEMALE = "W"
    NOT_DETERMINABLE = " "


class GenericInput(ABC):
    def __init__(
        self, df: pd.DataFrame, expected_columns: List[str], optional_columns: List[str]
    ):
        self.df = df
        self.expected_columns = expected_columns
        self.optional_columns = optional_columns

    @abstractmethod
    def normalize_input(
        self,
    ) -> OutputFileContainer:
        pass

    def handle_optional_columns(self):
        for optional_column in self.optional_columns:
            if optional_column not in self.df.columns:
                self.df[optional_column] = ""

    def validate_input(self):
        crit_in = all(
            [
                column in self.expected_columns + self.optional_columns
                for column in list(self.df.columns)
            ]
        )
        crit_out = all(
            [column in list(self.df.columns) for column in self.expected_columns]
        )

        return crit_in and crit_out
