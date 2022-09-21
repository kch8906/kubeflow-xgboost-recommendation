import csv
import argparse
import json
from importlib.resources import path
import numpy as np
import pandas as pd
import xgboost as xgb
import dill
import pickle
from tqdm import tqdm

def readJson(path: str):
    with open(f'{path}') as f:
        js = json.loads(f.read()) 
        df = pd.DataFrame(js)        

    return df


def test_model(model_path: path):

    with open(f'{model_path}', 'rb') as f:
        model = dill.load(f)

    return model

def predict(x_test: csv, y_test: csv, model: dill):
    dtest = xgb.DMatrix(data=x_test, label=y_test)
    pred_probs = model.predict(dtest)

    np.save('/tmp/pred_probs.npy', pred_probs)

    return pred_probs
    

# def extract_top5(pred_probs: np.array):

#     res = []
#     idx = []

#     for i in tqdm(range(len(pred_probs))):
#         res.append([])
#         idx.append([])
        
#         for j in range(len(pred_probs[i])):
#             if pred_probs[i][j] >= 0.1:
#                 res[i].append(pred_probs[i][j])
#                 idx[i].append(j)

#     return res, idx

# def accuracy_top5(idx, y_test, pred_probs) -> np.array:
    
#     count = 0
#     y_list = np.array(list(y_test))

#     for i in tqdm(range(len(pred_probs))):
#         if str(y_list[i] in idx[i]) == 'True':
#             count += 1
    
#     acc = count /len(pred_probs)

#     return acc



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_test')
    parser.add_argument('--y_test')
    parser.add_argument('--model')
    args = parser.parse_args()

    x_test = readJson(args.x_test)
    y_test = readJson(args.y_test)    
    model = test_model(args.model)
    pred_probs = predict(x_test, y_test, model)
    # res, idx = extract_top5(pred_probs)


    print(pred_probs)
    # print(res)
    # print(idx)
    # acc = accuracy_top5(idx, y_test, pred_probs)

    # print(f'Accuracy : {acc}')
    