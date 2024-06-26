import sys
import pandas as pd
import numpy as np

PATH = "../data/"

def add_animal(farm, animal):
    farm.add(animal)
    return farm

def main(animals):
    farm = set()
    df = pd.DataFrame()
    
    print(df)
    print(pd.read_csv(PATH+"dialysis.csv", encoding="ISO-8859-1"))
    # clean_data.print_string("hello world")
    for animal in animals:
        farm = add_animal(farm, animal)
    print("We've got some animals on the farm:", ','.join(farm) + '.')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Pass at least one animal type!')
        sys.exit(1)
    main(sys.argv[1:])
