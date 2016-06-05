from __future__ import division
import pandas as pd
from random import shuffle, choice



def split_data(data_file):

    df = pd.read_csv(data_file)

    training_size = int(0.4 * len(df))
    validation_size = int(0.2 * len(df))
    testing_size = int(0.4 * len(df))

    indexes = range(len(df))
    shuffle(indexes)

    training_indexes = indexes[:training_size]
    validation_indexes = indexes[training_size: training_size+validation_size]
    testing_indexes = indexes[training_size+validation_size:]

    training_data = [df.iloc[training_index] for training_index in training_indexes]
    validation_data = [df.iloc[validation_index] for validation_index in validation_indexes]
    testing_data = [df.iloc[testing_index] for testing_index in testing_indexes]

    assert(len(training_data) + len(validation_data) + len(testing_data) == len(df)), "Something is wrong"
    return training_data, validation_data, testing_data


def data_cleaning(filename):
    data_folder = "./Data/"
    data_file = data_folder + filename

    df = pd.read_csv(data_file)
    print "before cleaning"
    headers = [h for h in df.columns if '$<' not in h]
    for header in headers:
        try:df = df[df[header] != " NaN"]
        except:pass

    cleanded_filename = data_folder + "cleaned_"+filename
    df.to_csv(cleanded_filename , index=False)
    return cleanded_filename

def vectorizing(filename):
    # http://stackoverflow.com/questions/32011359/convert-categorical-data-in-pandas-dataframe
    df = pd.read_csv(filename)
    cat_columns = df.select_dtypes(['object']).columns
    for cat_column in cat_columns:
        df[cat_column] = df[cat_column].astype('category')
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    df.to_csv(filename, index=False)









