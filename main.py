import pandas as pd 
from pathlib import Path 

import argparse 
from src.henkel import normalize_henkel


def load_source_xlsx(path:Path):
    return pd.read_excel(path)
    
def validate_and_normalize_df(df:pd.DataFrame):

    assert len(df)>0 , f"The Excel seems to be empty"

    expected_cols_bookings = ['Date Time', 'Customer Name', 'Customer Email', 'Customer Phone',
       'Customer Address', 'Staff', 'Staff Name', 'Staff Email', 'Service',
       'Location', 'Duration (mins.)', 'Pricing Type', 'Price', 'Currency',
       'Cc Attendees', 'Signed Up Attendees Count',
       'Text Notifications Enabled', ' Custom Fields', 'Event Type',
       'Booking Id', 'Tracking Data']
    
    if list(df.columns) == expected_cols_bookings:
        return normalize_henkel(df)
        # determine_gender by first name
                

    elif list(df.columns) == expected_cols_something: 
        pass

    else:
        raise ValueError(f"expected columns to be {expected_cols_bookings} or {expected_cols_something} but is {list(df.columns)}")



def main(args):
    source_file = Path(args.source_file)
    target_dir = source_file.parent
    df = load_source_xlsx(source_file)

    df_labor = validate_and_normalize_df(df)
    
    path_labor_file = target_dir/ (source_file.stem+ "_Labor")
    df_labor.to_csv(path_labor_file, index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("--source-file", "-s")

    args = parser.parse_args()
    main(args)




    