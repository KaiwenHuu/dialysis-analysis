import pandas as pd
import numpy as np
import zipfile

CATEGORICAL = "categorical.txt"
BINARY = "binary.txt"
OUTCOME = "outcome.txt"
DROP = "drop.txt"

def load_dataset(path, filename):
    categ = open(f"{path}{CATEGORICAL}", 'r').read().replace('\n', '').split(",")
    binary = open(f"{path}{BINARY}", 'r').read().replace('\n', '').split(",")
    drop = open(f"{path}{DROP}", 'r').read().replace('\n', '').split(",")
    outcome = open(f"{path}{OUTCOME}", 'r').read().replace('\n', '').split(",")

    data = None
    zipfilepath = f"{path}{filename}.zip"
    with zipfile.ZipFile(zipfilepath, 'r') as zip_ref:
        with zip_ref.open(f"{filename}.csv") as file:
            data = pd.read_csv(file)

    # write all variables into a text file
    with open(f"{path}unique_values.txt", 'w') as f:
        for column in data.columns:
            unique_values = data[column].unique()
            f.write(f"Unique values in '{column}': {unique_values}\n")
    
    # change true false to 0, 1
    for bin in binary:
        data[bin] = np.where(data[bin] == True, 1, 0)

    # drop unnecessary columns    
    data = data.drop(columns = drop)

    # observations with nans
    data = data.dropna()

    with open(f"{path}unique_values_cleaned.txt", 'w') as f:
        for column in data.columns:
            unique_values = data[column].unique()
            f.write(f"Unique values in '{column}': {unique_values}\n")

    X = data.drop(columns=outcome).to_numpy()

    y = data[outcome].to_numpy()
    
    return X, y