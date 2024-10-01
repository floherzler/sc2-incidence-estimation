import pandas as pd
import subprocess
import os
import tqdm
import argparse

# keep only first column

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='The name of the file to read')
    parser.add_argument('dir_name', type=str, help='The name of the directory to save the fastas')
    dir_name = parser.parse_args().dir_name
    ids = pd.read_csv(parser.parse_args().filename)
    # keep only first column
    ids = ids.iloc[:,0]
    # create out dir
    os.makedirs(f'../data/fastas/{dir_name}', exist_ok=True)
    for id in tqdm.tqdm(ids):
        # Ensure the directory exists
        os.makedirs('../data/fastas', exist_ok=True)
        with open(f'../data/fastas/{dir_name}/{id}.fasta', 'x') as output_file:
            subprocess.run(['../pipelines/covsonar/sonar.py', 'restore', '--acc', id, '--db', '../data/given/france/project4.db'], stdout=output_file)
