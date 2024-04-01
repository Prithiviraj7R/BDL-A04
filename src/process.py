# importing necessary libraries

import pandas as pd
import numpy as np
import os
import yaml
from datetime import datetime

def compute_monthly_averages(input_folder, hourly_features, monthly_features, extraction_folder, output_folder):
    """
    Function to compute the monthly averages for the features 
    extracted in the preparation stage and store the computed
    aggregates in the designated folder.

    Args:
        input_folder (str): Path to the folder containing input data files.
        hourly_features (list): List of features to compute hourly averages for.
        monthly_features (list): List of corresponding monthly features.
        extraction_folder (str): Path to the folder where extracted data is stored.
        output_folder (str): Path to the folder to store computed averages.

    Returns:
        None    
    """
    files = os.listdir(extraction_folder)
    files = [file for file in files if not file.startswith('computed')]

    for file_name in files:
        file_path = os.path.join(extraction_folder, file_name)
        monthly_features_df = pd.read_csv(file_path, low_memory=False)
        monthly_columns = monthly_features_df.columns

        # get the hourly features to be aggregated month wise

        hourly_columns = [
            hourly_feature 
            for hourly_feature, monthly_feature
            in zip(hourly_features, monthly_features)
            if monthly_feature in monthly_columns
        ]

        computed_df = pd.DataFrame()
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path, low_memory=False)

        # computation of monthly averages

        for hourly_column in hourly_columns:
            computed_monthly_averages = {i: 0.0 for i in range(1,13)}

            dates = df['DATE']
            dates = np.array([datetime.strptime(date, r"%Y-%m-%dT%H:%M:%S") for date in dates])
            months = [date.month for date in dates]
            unique_months = set(months)

            hourly_data = df[hourly_column]
            hourly_data = pd.to_numeric(hourly_data, errors='coerce')

            for month in unique_months:
                indices = [i for i, m in enumerate(months) if m == month]
                monthly_data = hourly_data[indices]
                monthly_average = np.mean(monthly_data, axis=0)
                computed_monthly_averages[month] = monthly_average

            sorted_months = sorted(computed_monthly_averages.keys())
            sorted_averages = [computed_monthly_averages[month] for month in sorted_months]
                
            computed_df[hourly_column] = sorted_averages

        # save the computed monthly averages as a csv file

        output_file_path = os.path.join(output_folder, f'computed_{file_name}')
        computed_df.to_csv(output_file_path, index=False, mode='w')


def main():
    # Load the required parameters
    params = yaml.safe_load(open("params.yaml"))["download"]

    input_folder = params['destination']
    hourly_features = params['hourly_features']
    monthly_features = params['monthly_features']
    extraction_folder = 'data/output/'
    output_folder = 'data/computed/'

    os.makedirs(output_folder, exist_ok=True)
    
    compute_monthly_averages(
        input_folder,
        hourly_features,
        monthly_features,
        extraction_folder,
        output_folder,
    )

if __name__ == '__main__':
    main()