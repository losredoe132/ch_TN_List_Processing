import pandas as pd 
from pathlib import Path 

import argparse 
from typing import Tuple
from src.bookings import normalize_bookings_df, expected_colums_bookings


def load_source_xlsx(path:Path):
    return pd.read_excel(path)
    
def validate_and_normalize_df(df:pd.DataFrame)-> Tuple[pd.DataFrame, pd.DataFrame]:

    assert len(df)>0 , f"The Excel seems to be empty"


    if list(df.columns) == expected_colums_bookings:
        return normalize_bookings_df(df)                

    elif list(df.columns) == expected_columns_portal: 
        pass

    else:
        raise ValueError(f"expected columns to be {expected_colums_bookings} or {expected_cols_something} but is {list(df.columns)}")



def main(source_file):
    source_file = Path(source_file)
    target_dir = source_file.parent
    df = load_source_xlsx(source_file)

    df_labor, df_accounting = validate_and_normalize_df(df)
    
    path_labor = target_dir/ (source_file.stem+ "_Labor.csv")
    df_labor.to_csv(path_labor, index=False)

    path_accounting = target_dir/ (source_file.stem+ "_Buchhaltung.xlsx")
    df_accounting.to_excel(path_accounting, index=False)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("--source-file", "-s")

    args = parser.parse_args()
    main(source_file = args.source_file)




    