# importing necessary libraries

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from dvclive import Live
import os
import yaml

def evaluate(input_folder, computed_folder, live, save_path):
    """
    Function to evaluate the performance of computed features against ground truth data.

    Args:
        input_folder (str): Path to the folder containing ground truth data files.
        computed_folder (str): Path to the folder containing computed data files.
        live (dvclive.Live): Instance of dvclive.Live for live logging.
        save_path (str): Path to save evaluation results.

    Returns:
        None
    """

    files = os.listdir(input_folder)
    computed_files = os.listdir(computed_folder)

    # computed_files = [file_name for file_name in files if file_name.startswith('computed')]
    gt_files = [file_name for file_name in files if file_name not in computed_files]

    r2_values= []

    for gt_file, computed_file in zip(gt_files, computed_files):
        gt_path = os.path.join(input_folder, gt_file)
        computed_path = os.path.join(computed_folder, computed_file)
        gt_df = pd.read_csv(gt_path)
        computed_df = pd.read_csv(computed_path)

        gt_features = gt_df.columns
        computed_features = computed_df.columns
        local_r2_scores = []

        for gt_feature, computed_feature in zip(gt_features, computed_features):
            valid_rows_gt = gt_df[gt_feature] != 0.0
            gt_values = gt_df.loc[valid_rows_gt, gt_feature]
            computed_values = computed_df.loc[valid_rows_gt, computed_feature]

            r2 = r2_score(gt_values, computed_values)
            local_r2_scores.append(r2)

        average_score = sum(local_r2_scores)/len(local_r2_scores)
        r2_values.append(average_score)

    global_average = sum(r2_values)/len(r2_values)

    if not live.summary:
        live.summary = {'R2': {}, 'Consistency': {}}
    live.summary['R2'] = global_average
    if global_average > 0.90:
        live.summary['Consistency'] = 'C'
    else:
        live.summary['Consistency'] = 'NC'
    

def main():
    # parameters for evaluation
    input_folder = 'data/output/'
    computed_folder = 'data/computed/'
    EVAL_PATH = 'eval'

    # Live staging for experimentation 
    with Live(EVAL_PATH, dvcyaml=False) as live:
        evaluate(input_folder, computed_folder, live, save_path=EVAL_PATH)

if __name__ == '__main__':
    main()