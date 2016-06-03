from src.data_splitting import split_data, data_cleaning, vectorizing

if __name__ == "__main__":
    # split_data("adult.csv")
    filename = data_cleaning("bankecho "# Tuning" >> README.md.csv")
    vectorizing(filename)