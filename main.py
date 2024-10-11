import pandas as pd 
from pathlib import Path 

import argparse 



def create_target_xlsxs(df:pd.DataFrame,target_dir : Path ):
    # create female table 
    pass

def load_source_xlsx(path:Path):
    return pd.read_excel(path)
    
def validate_df(df:pd.DataFrame):
    expected_cols = ['Date Time', 'Customer Name', 'Customer Email', 'Customer Phone',
       'Customer Address', 'Staff', 'Staff Name', 'Staff Email', 'Service',
       'Location', 'Duration (mins.)', 'Pricing Type', 'Price', 'Currency',
       'Cc Attendees', 'Signed Up Attendees Count',
       'Text Notifications Enabled', ' Custom Fields', 'Event Type',
       'Booking Id', 'Tracking Data']
    assert list(df.columns) == expected_cols, f"Columns of the Excel Sheet are not as expected: Expected: {expected_cols}\n Actual: {list(df.columns)}\n"
    assert len(df)>0 , f"The Excel seems to be empty"


def main(args):
    source_file = Path(args.source_file)
    target_dir = source_file.parent
    df = load_source_xlsx(source_file)

    validate_df(df)

    create_target_xlsxs(df, target_dir=target_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("--source-file", "-s")

    args = parser.parse_args()
    main(args)




    