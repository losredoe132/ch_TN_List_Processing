# Cooperate Health 

## Setup 
```
python -m venv .venv

# UNIX only
source .venv/bin/activate

# WINDOWS only
.\.venv\Scripts\activate

pip install requirements/requirements.txt

# development only
pip install requirements/dev.txt 
```


## Extend Names List
In the folder `data` there are two json files. If you would like to add a name to one of these list, just add it and follow the formating.
Names that are present in both list, the script will not assign any gender to the corresponding row.  


## Run 
Python Version: 3.8.10

Start a terminal in the root directory of this repo. And call it like: 

`python main.py -s <SOURCE_FILE>`

for example: 

`python main.py -s /home/finn/Desktop/TN-Liste_Codierung_AK.xlsx`