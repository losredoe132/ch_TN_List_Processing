import argparse
import logging
from pathlib import Path

import pandas as pd

from src.bookings import BookingsInput
from src.common import OutputFileContainer, load_source
from src.portal import PortalInput

# Configure the logger
logger = logging.getLogger("example_logger")
logger.setLevel(logging.DEBUG)


def validate_and_normalize_df(df: pd.DataFrame) -> OutputFileContainer:
    assert len(df) > 0, "The Excel seems to be empty"
    bookings_input = BookingsInput(df)
    portal_input = PortalInput(df)

    logger.info("Determin input format")
    if bookings_input.validate_input():
        logger.info("Matched Source as 'Bookings' Input")
        return bookings_input.normalize_input()
    elif portal_input.validate_input():
        logger.info("Matched Source as 'Portal' Input")
        return portal_input.normalize_input()

    else:
        raise ValueError(f"no matching input format for {df.columns}")


def main(source_file):
    source_file = Path(source_file)
    assert (
        len(source_file.name) < 250
    ), f"""Length of source path is {len(source_file.name)} >250!. 
    On windows this is too long to be saved as target. Move this directory to a shorter path."""

    target_dir = source_file.parent
    df = load_source(source_file)

    output_dfs = validate_and_normalize_df(df)

    df_accounting = output_dfs.accounting
    df_labor = output_dfs.labor
    df_labor_male = df_labor[df_labor["Geschlecht"] == "M"]
    df_labor_female = df_labor[df_labor["Geschlecht"] == "W"]

    path_labor = target_dir / (source_file.stem + "_Labor_M.csv")
    df_labor_male.to_csv(path_labor, index=False, decimal=",", sep=";")

    path_labor = target_dir / (source_file.stem + "_Labor_F.csv")
    df_labor_female.to_csv(path_labor, index=False, decimal=",", sep=",")

    path_accounting = target_dir / (source_file.stem + "_Buchhaltung.xlsx")
    df_accounting.to_excel(path_accounting, index=False)
    logging.info(f"Finished successfully and saved to {target_dir}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("--source-file", "-s")

    args = parser.parse_args()
    main(source_file=args.source_file)
