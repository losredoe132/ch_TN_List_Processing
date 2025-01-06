import argparse
import logging
from pathlib import Path

import pandas as pd

from src.bookings import expected_colums_bookings, normalize_bookings_df
from src.common import OutputFileContainer, load_source
from src.portal import expected_columns_portal, normalize_portal_df


def validate_and_normalize_df(df: pd.DataFrame) -> OutputFileContainer:
    assert len(df) > 0, "The Excel seems to be empty"

    if list(df.columns) == expected_colums_bookings:
        logging.info("Matched Source as 'Bookings' Input")
        return normalize_bookings_df(df)

    elif list(df.columns) == expected_columns_portal:
        logging.info("Matched Source as 'Portal' Input")
        return normalize_portal_df(df)

    else:
        raise ValueError(
            f"expected columns to be\n{expected_colums_bookings}\nor\n{expected_columns_portal}\nbut is\n{list(df.columns)}"
        )


def main(source_file):
    source_file = Path(source_file)
    target_dir = source_file.parent
    df = load_source(source_file)

    output_dfs = validate_and_normalize_df(df)

    df_accounting = output_dfs.accounting
    df_labor = output_dfs.labor
    df_labor_male = df_labor[df_labor["Geschlecht"] == "M"]
    df_labor_female = df_labor[df_labor["Geschlecht"] == "W"]

    path_labor = target_dir / (source_file.stem + "_Labor_M.csv")
    df_labor_male.to_csv(path_labor, index=False)

    path_labor = target_dir / (source_file.stem + "_Labor_F.csv")
    df_labor_female.to_csv(path_labor, index=False)

    path_accounting = target_dir / (source_file.stem + "_Buchhaltung.xlsx")
    df_accounting.to_excel(path_accounting, index=False)
    logging.info("Finished successfully")


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
