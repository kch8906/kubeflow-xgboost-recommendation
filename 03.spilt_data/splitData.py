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
    
   
    np.save('/tmp/x_test.npy', X_test)    
    np.save('/tmp/y_test.npy', y_test)
    np.save('/tmp/x_tr.npy', X_tr)
    np.save('/tmp/x_val.npy', X_val)
    np.save('/tmp/y_tr.npy', y_tr)
    np.save('/tmp/y_val.npy', y_val)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--df')
    args = parser.parse_args()

    df = readJson(args.df)
    split_train_test(df)



