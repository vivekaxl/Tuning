from src.data_splitting import split_data, data_cleaning, vectorizing
import pandas as pd
from os import listdir

def cleaning():
    filename = data_cleaning("bank.csv")
    vectorizing(filename)

def normalization(filename):
    foldername = "./norm_data/"
    df = pd.read_csv(filename)
    columns = df.columns
    independent = columns[:-1]
    dependent = columns[-1]
    independent_df = df[independent]
    df_norm = (independent_df - independent_df.mean()) / (independent_df.max() - independent_df.min())
    df_norm['class'] = df[dependent]
    df_norm.to_csv(foldername + filename.split("/")[-1], index=False)


def _normalization():
    foldername = "./Data/"
    files = [foldername + f for f in listdir(foldername)]
    files.remove('./Data/.DS_Store')
    files.remove('./Data/__init__.py')
    for file in files:
        normalization(file)

if __name__ == "__main__":