import pandas as pd
import numpy as np
import zipfile

CATEGORICAL = "categorical.txt"
BINARY = "binary.txt"
OUTCOME = "outcome.txt"
SURVEYDT_F = "surveydt_f"
INSPECTION_DATES = "inspection_dates"

def load_dataset(path, filename):
    categ = open(f"{path}{CATEGORICAL}", 'r').read().replace('\n', '').split(",")
    binary = open(f"{path}{BINARY}", 'r').read().replace('\n', '').split(",")
    outcome = open(f"{path}{OUTCOME}", 'r').read().replace('\n', '').split(",")

    data = None
    zipfilepath = f"{path}{filename}.zip"
    with zipfile.ZipFile(zipfilepath, 'r') as zip_ref:
        with zip_ref.open(f"{filename}.csv") as file:
            data = pd.read_csv(file)

    with open(f"{path}unique_values.txt", 'w') as f:
        for column in data.columns:
            unique_values = data[column].unique()
            f.write(f"Unique values in '{column}': {unique_values}\n")
    
    for bin in binary:
        print(bin)
        data[bin] = np.where(data[bin] == True, 1, 0)

    data_with_categ = pd.concat([
        data.drop(columns=categ), # dataset without the categorical features
        pd.get_dummies(data[categ], columns=categ, drop_first=False)# categorical features converted to dummies
    ], axis=1)

    data_with_categ[SURVEYDT_F] = pd.to_datetime(data_with_categ[SURVEYDT_F])
    data_with_categ[SURVEYDT_F] = (data_with_categ[SURVEYDT_F] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')

    data_with_categ = data_with_categ.fillna(0)

    with open(f"{path}unique_values_cleaned.txt", 'w') as f:
        for column in data_with_categ.columns:
            unique_values = data_with_categ[column].unique()
            f.write(f"Unique values in '{column}': {unique_values}\n")

    X = data_with_categ.drop(columns=outcome + [INSPECTION_DATES]).to_numpy()

    y = data_with_categ[outcome].to_numpy()
    
    return X, y