import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
import json


def readJson(path: str):
    with open(f'{path}') as f:
        js = json.loads(f.read()) 
        df = pd.Series(js)        

    return df


def accuracy_top(y_test: pd.Series, pred_probs: np.array, n: int):
    pred_copy = pred_probs.copy()
    idx=[]
    for i in range(len(pred_copy)):
        sort_values = pred_copy[i].argsort()
        idx.append(sort_values[:: -1][:n].tolist())

    result = 0    
    y_list = list(y_test)

    for j in range(len(y_list)):
        if y_list[j] in idx[j]:
            result += 1

    acc = result / len(pred_copy)

    return acc


def export_metric(acc_top5, acc_top10):
    metrics = {
        "metrics": [
            {
                "name": "Accuracy_Top5",
                "numberValue": acc_top5,
                "format": "PERCENTAGE",
            },
            {
                "name": "Accuracy_Top10",
                "numberValue": acc_top10,
                "format": "PERCENTAGE",
            }
        ]
    }

    with open("/tmp/metrics.json", "w") as f:
        json.dump(metrics, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred_probs')
    parser.add_argument('--y_test')
    args = parser.parse_args()

    pred_probs = np.load(args.pred_probs)
    y_test = readJson(args.y_test)

    acc_top5 = accuracy_top(y_test, pred_probs, 5)
    acc_top10 = accuracy_top(y_test, pred_probs, 10)

    export_metric(acc_top5, acc_top10)
