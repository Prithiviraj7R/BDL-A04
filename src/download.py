# importing necessary libraries

import os
import yaml
import numpy as np
import pandas as pd
import requests
import subprocess
from bs4 import BeautifulSoup


def fetch_file_links(html_file, n_files, seed):
    """
    Function to parse the HTML file extracted using Bash operator from the archive URL and 
    it retrieves the links for the .csv files in the HTML file and returns
    the list of links to be downloaded.

    Args:
    html_file (str): Path to the HTML file to be parsed.
    n_files (int): Number of files to randomly select.
    seed (int): Seed for the random number generator.
    
    Returns:
    list: List of randomly selected file links.
    """
    with open(html_file, "r") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    file_links = [link.get("href") for link in soup.find_all("a")]
    file_links = [link for link in file_links if link.endswith('.csv')]

    selected_files = np.random.RandomState(seed).choice(file_links, size=n_files)

    return selected_files


def check_validity(file, monthly_features, hourly_features):
    """
    Function to check if the downloaded csv file contains a 
    non-empty monthly average column and a corresponding hourly 
    data.

    Args:
    file (str): Path to the csv file to be validated
    monthly_features (list): List of monthly features to check
    hourly_features (list): List of corresponding hourly features

    Returns:
    bool: True if the file is valid and can be used for processing
    """

    df = pd.read_csv(file, low_memory=False)
    columns = df.columns

    for monthly_feature, hourly_feature in zip(monthly_features, hourly_features):
        if monthly_feature in columns:
            non_empty_column = df[monthly_feature].notna()
            if non_empty_column.any():
                if hourly_feature in columns:
                    non_empty_hourly = df[hourly_feature].notna()
                    if non_empty_hourly.any():
                        return True
    
    return False

    
def fetch_data(files, destination, base_url, year, monthly_features, hourly_features):
    """
    Function to download the content from all the .csv files and
    stores the files in a folder that will be zipped in the next task.

    Args:
    files (list): List of file names to be downloaded.
    destination (str): Path to the folder where the files will be stored.
    base_url (str): Base URL of the web archive.
    year (int): Year of the archive.
    monthly_features (list): List of monthly features to check for validity.
    hourly_features (list): List of corresponding hourly features.

    Returns:
    list: List of valid file names.
    """
    os.makedirs(destination, exist_ok=True)
    valid_files = []
    count = i = 0

    for file in files:
        file_path = f'{destination}{file}'
        file_link = f'{base_url}{year}/{file}'

        response = requests.get(file_link)

        with open(file_path, "wb") as f:
            f.write(response.content)
            print(f'Downloaded [{i+1}/{len(files)}]')
            i += 1

        # checking the file for non-empty monthly features

        if check_validity(file_path, monthly_features, hourly_features):
            valid_files.append(file_path)
            count += 1

            if count >= 3:
                return valid_files
        else:
            os.remove(file_path)

    return valid_files


def main():
    # Load the required parameters
    
    params = yaml.safe_load(open("params.yaml"))["download"]

    base_url = params["base_url"]
    link_parse_file = params["link_parser"]
    destination = params["destination"]
    year = params["year"]
    n_locs = params["n_locs"]
    seed = params["seed"]
    monthly_features = params["monthly_features"]
    hourly_features = params["hourly_features"]

    os.makedirs(destination, exist_ok=True)

    # Fetch the links from the location

    fetch_command = f'curl -o {link_parse_file} {base_url}{year}/'

    try:
        subprocess.run(fetch_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")

    selected_files = fetch_file_links(link_parse_file, n_locs, seed)
    valid_files = fetch_data(selected_files, destination, base_url, year, monthly_features, hourly_features)

if __name__ == '__main__':
    main()
    

    

    



