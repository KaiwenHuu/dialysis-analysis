import sys
import pandas as pd
import numpy as np

from utils import (
    load_dataset
)

PATH = "../data/"
FILENAME = "dialysis"

def add_animal(farm, animal):
    farm.add(animal)
    return farm

def main(animals):
    farm = set()
    
    X, y = load_dataset(PATH, FILENAME)
    print(X.shape)
    print(y.shape)
    for animal in animals:
        farm = add_animal(farm, animal)
    print("We've got some animals on the farm:", ','.join(farm) + '.')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Pass at least one animal type!')
        sys.exit(1)
    main(sys.argv[1:])
