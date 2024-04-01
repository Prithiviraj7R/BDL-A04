# importing necessary libraries

import pandas as pd
import numpy as np
import yaml
import os
from datetime import datetime

def extract_monthly_features(input_folder, output_folder, hourly_features, monthly_features):
    """
    Function to extract monthly features from input data files and 
    store the extracted features in a specified output folder.

    Args:
        input_folder (str): Path to the folder containing input data files.
        output_folder (str): Path to the folder where extracted features will be stored.
        hourly_features (list): List of features to compute hourly averages for.
        monthly_features (list): List of corresponding monthly features.

    Returns:
        None
    """

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path, low_memory=False)
        monthly_df = pd.DataFrame()

        # check for non-empty monthly features and corresponding hourly features

        for monthly_feature, hourly_feature in zip(monthly_features, hourly_features):
            if monthly_feature in df.columns:
                non_empty_column = df[monthly_feature].notna()
                if non_empty_column.any():
                    if hourly_feature in df.columns:
                        non_empty_hourly = df[hourly_feature].notna()
                        if non_empty_hourly.any():
                            monthly_data = df[monthly_feature][non_empty_column].tolist()
                            months = df.loc[non_empty_column, 'DATE'].apply(lambda x: datetime.strptime(x, r"%Y-%m-%dT%H:%M:%S").month).to_numpy()

                            monthly_data_dict = {month: 0.0 for month in range(1, 13)}

                            for i,month in enumerate(months):
                                monthly_data_dict[month] = monthly_data[i]
                            monthly_data = list(monthly_data_dict.values())

                            monthly_df[monthly_feature] = monthly_data            
                        
        # store the extracted file containing the monthly averages
        output_file_path = os.path.join(output_folder, file_name)
        monthly_df.to_csv(output_file_path, index=False)

        
def main():
    # Load the required parameters
    params = yaml.safe_load(open("params.yaml"))["download"]

    input_folder = params['destination']
    hourly_features = params['hourly_features']
    monthly_features = params['monthly_features']

    output_folder = 'data/output/'
    os.makedirs(output_folder, exist_ok=True)

    extract_monthly_features(input_folder, output_folder, hourly_features, monthly_features)


if __name__ == '__main__':
    main()