import argparse
import logging
from pathlib import Path

from src.common import load_source_xlsx, validate_and_normalize_df


def main(source_file):
    source_file = Path(source_file)
    target_dir = source_file.parent
    df = load_source_xlsx(source_file)

    df_labor, df_accounting = validate_and_normalize_df(df)

    path_labor = target_dir / (source_file.stem + "_Labor.csv")
    df_labor.to_csv(path_labor, index=False)

    path_accounting = target_dir / (source_file.stem + "_Buchhaltung.xlsx")
    df_accounting.to_excel(path_accounting, index=False)


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
