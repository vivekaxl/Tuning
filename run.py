from src.data_splitting import split_data, data_cleaning, vectorizing
import pandas as pd

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
    import pdb
    pdb.set_trace()


if __name__ == "__main__":

