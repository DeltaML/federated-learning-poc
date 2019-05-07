import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("diabetes.csv", header=None)
    n = 50
    list_df = [df[i:i + n] for i in range(0, df.shape[0], n)]
    data_frame = df.drop(index=0)
    for idx, val in enumerate(list_df):
        val.to_csv(path_or_buf="file_{}.csv".format(idx), index=False, header=None)
