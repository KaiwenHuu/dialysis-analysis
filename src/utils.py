import pandas as pd
import numpy as np
import zipfile

CATEGORICAL = "categorical.txt"
BINARY = "binary.txt"

def load_dataset(path, filename):
    categ = open(f"{path}{CATEGORICAL}", 'r').read().replace('\n', '').split(",")
    binary = open(f"{path}{BINARY}", 'r').read().replace('\n', '').split(",")

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

    data_with_categ = data_with_categ.fillna(0)
    
    return data