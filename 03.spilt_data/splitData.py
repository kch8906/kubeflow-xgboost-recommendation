import argparse
import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split


def readJson(path: str):
    with open(f'{path}') as f:
        js = json.loads(f.read()) 
        df = pd.DataFrame(js)        

    return df


def split_train_test(df: pd.DataFrame):
    x = df.drop(columns='clac_hlv_nm', axis=1)
    y = df['clac_hlv_nm']
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=156)
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=156)
    
    X_tr.to_json("/tmp/x_tr.json", orient = "records")
    y_tr.to_json("/tmp/y_tr.json", orient = "records")
    X_val.to_json("/tmp/x_val.json", orient = "records")
    y_val.to_json("/tmp/y_val.json", orient = "records")
    X_test.to_json("/tmp/x_test.json", orient = "records")
    y_test.to_json("/tmp/y_test.json", orient = "records")



if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    args = parser.parse_args()

    df = readJson(args.df)
    split_train_test(df)



