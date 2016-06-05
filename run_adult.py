from src.data_splitting import split_data, data_cleaning, vectorizing, split_data
from src.de import run_random_forest, run_de_4_rf
import pandas as pd
from random import seed
from os import listdir
from numpy import mean, std

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


def run_experiment(files):
    seed(15)
    de_parameters = {
        "lives": 5,
        "pop_size": 10,
        "max_generations": 10,
        "F":0.3,
        "CF":0.7

    }

    untuned_parameter = [10, 2, 1, None, 'auto']
    for file in files:
        untuned_scores = []
        tuned_scores = []

        for _ in xrange(10):
            train, val, test = split_data(file)
            parameter = run_de_4_rf(train, val, de_parameters)
            untuned_scores.append(run_random_forest(train, test, untuned_parameter))
            tuned_scores.append(run_random_forest(train, test, parameter))

        result_file = "./Results/" + file.split("/")[-1]
        string = ""
        string += file.split("/")[-1] + "\n"
        string += "untuned: " + str(mean(untuned_scores)) + " " + str(std(untuned_scores)) + "\n"
        string += "tuned: " + str(mean(tuned_scores)) + " " + str(std(tuned_scores)) + "\n"
        fd = open(result_file, "w")
        fd.write(string)
        fd.close()

if __name__ == "__main__":
    run_experiment("./norm_data/cleaned_adult.csv")